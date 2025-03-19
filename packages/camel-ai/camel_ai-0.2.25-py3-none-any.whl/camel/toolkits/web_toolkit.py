# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

import datetime
import io
import json
import os
import random
import re
import shutil
import time
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    List,
    Optional,
    Tuple,
    TypedDict,
    Union,
    cast,
)

from PIL import Image, ImageDraw, ImageFont

if TYPE_CHECKING:
    from camel.agents import ChatAgent
from camel.logger import get_logger
from camel.messages import BaseMessage
from camel.models import BaseModelBackend, ModelFactory
from camel.toolkits import FunctionTool, VideoAnalysisToolkit
from camel.toolkits.base import BaseToolkit
from camel.types import ModelPlatformType, ModelType
from camel.utils import dependencies_required, retry_on_error

logger = get_logger(__name__)

TOP_NO_LABEL_ZONE = 20

AVAILABLE_ACTIONS_PROMPT = """
1. `fill_input_id(identifier: Union[str, int], text: str)`: Fill an input 
field (e.g. search box) with the given text and press Enter.
2. `click_id(identifier: Union[str, int])`: Click an element with the given ID.
3. `hover_id(identifier: Union[str, int])`: Hover over an element with the 
given ID.
4. `download_file_id(identifier: Union[str, int])`: Download a file with the 
given ID. It returns the path to the downloaded file. If the file is 
successfully downloaded, you can stop the simulation and report the path to 
the downloaded file for further processing.
5. `scroll_to_bottom()`: Scroll to the bottom of the page.
6. `scroll_to_top()`: Scroll to the top of the page.
7. `scroll_up()`: Scroll up the page. It is suitable when you want to see the 
elements above the current viewport.
8. `scroll_down()`: Scroll down the page. It is suitable when you want to see 
the elements below the current viewport. If the webpage does not change, It 
means that the webpage has scrolled to the bottom.
9. `back()`: Navigate back to the previous page. This is useful when you want 
to go back to the previous page, as current page is not useful.
10. `stop()`: Stop the action process, because the task is completed or failed 
(impossible to find the answer). In this situation, you should provide your 
answer in your output.
11. `get_url()`: Get the current URL of the current page.
12. `find_text_on_page(search_text: str)`: Find the next given text on the 
current whole page, and scroll the page to the targeted text. It is equivalent 
to pressing Ctrl + F and searching for the text, and is powerful when you want 
to fast-check whether the current page contains some specific text.
13. `visit_page(url: str)`: Go to the specific url page.
14. `click_blank_area()`: Click a blank area of the page to unfocus the 
current element. It is useful when you have clicked an element but it cannot 
unfocus itself (e.g. Menu bar) to automatically render the updated webpage.
15. `ask_question_about_video(question: str)`: Ask a question about the 
current webpage which contains video, e.g. youtube websites.
"""

ACTION_WITH_FEEDBACK_LIST = [
    'ask_question_about_video',
    'download_file_id',
    'find_text_on_page',
]


# codes from magentic-one
class DOMRectangle(TypedDict):
    x: Union[int, float]
    y: Union[int, float]
    width: Union[int, float]
    height: Union[int, float]
    top: Union[int, float]
    right: Union[int, float]
    bottom: Union[int, float]
    left: Union[int, float]


class VisualViewport(TypedDict):
    height: Union[int, float]
    width: Union[int, float]
    offsetLeft: Union[int, float]
    offsetTop: Union[int, float]
    pageLeft: Union[int, float]
    pageTop: Union[int, float]
    scale: Union[int, float]
    clientWidth: Union[int, float]
    clientHeight: Union[int, float]
    scrollWidth: Union[int, float]
    scrollHeight: Union[int, float]


class InteractiveRegion(TypedDict):
    tag_name: str
    role: str
    aria_name: str
    v_scrollable: bool
    rects: List[DOMRectangle]


def _get_str(d: Any, k: str) -> str:
    val = d[k]
    assert isinstance(val, str)
    return val


def _get_number(d: Any, k: str) -> Union[int, float]:
    val = d[k]
    assert isinstance(val, int) or isinstance(val, float)
    return val


def _get_bool(d: Any, k: str) -> bool:
    val = d[k]
    assert isinstance(val, bool)
    return val


def _parse_json_output(text: str) -> Dict[str, Any]:
    r"""Extract JSON output from a string."""

    markdown_pattern = r'```(?:json)?\s*(.*?)\s*```'
    markdown_match = re.search(markdown_pattern, text, re.DOTALL)
    if markdown_match:
        text = markdown_match.group(1).strip()

    triple_quotes_pattern = r'"""(?:json)?\s*(.*?)\s*"""'
    triple_quotes_match = re.search(triple_quotes_pattern, text, re.DOTALL)
    if triple_quotes_match:
        text = triple_quotes_match.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            fixed_text = re.sub(
                r'`([^`]*?)`(?=\s*[:,\[\]{}]|$)', r'"\1"', text
            )
            return json.loads(fixed_text)
        except json.JSONDecodeError:
            result = {}
            try:
                bool_pattern = r'"(\w+)"\s*:\s*(true|false)'
                for match in re.finditer(bool_pattern, text, re.IGNORECASE):
                    key, value = match.groups()
                    result[key] = value.lower() == "true"

                str_pattern = r'"(\w+)"\s*:\s*"([^"]*)"'
                for match in re.finditer(str_pattern, text):
                    key, value = match.groups()
                    result[key] = value

                num_pattern = r'"(\w+)"\s*:\s*(-?\d+(?:\.\d+)?)'
                for match in re.finditer(num_pattern, text):
                    key, value = match.groups()
                    try:
                        result[key] = int(value)
                    except ValueError:
                        result[key] = float(value)

                empty_str_pattern = r'"(\w+)"\s*:\s*""'
                for match in re.finditer(empty_str_pattern, text):
                    key = match.group(1)
                    result[key] = ""

                if result:
                    return result

                logger.warning(f"Failed to parse JSON output: {text}")
                return {}
            except Exception as e:
                logger.warning(f"Error while extracting fields from JSON: {e}")
                return {}


def _reload_image(image: Image.Image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return Image.open(buffer)


def domrectangle_from_dict(rect: Dict[str, Any]) -> DOMRectangle:
    return DOMRectangle(
        x=_get_number(rect, "x"),
        y=_get_number(rect, "y"),
        width=_get_number(rect, "width"),
        height=_get_number(rect, "height"),
        top=_get_number(rect, "top"),
        right=_get_number(rect, "right"),
        bottom=_get_number(rect, "bottom"),
        left=_get_number(rect, "left"),
    )


def interactiveregion_from_dict(region: Dict[str, Any]) -> InteractiveRegion:
    typed_rects: List[DOMRectangle] = []
    for rect in region["rects"]:
        typed_rects.append(domrectangle_from_dict(rect))

    return InteractiveRegion(
        tag_name=_get_str(region, "tag_name"),
        role=_get_str(region, "role"),
        aria_name=_get_str(region, "aria-name"),
        v_scrollable=_get_bool(region, "v-scrollable"),
        rects=typed_rects,
    )


def visualviewport_from_dict(viewport: Dict[str, Any]) -> VisualViewport:
    return VisualViewport(
        height=_get_number(viewport, "height"),
        width=_get_number(viewport, "width"),
        offsetLeft=_get_number(viewport, "offsetLeft"),
        offsetTop=_get_number(viewport, "offsetTop"),
        pageLeft=_get_number(viewport, "pageLeft"),
        pageTop=_get_number(viewport, "pageTop"),
        scale=_get_number(viewport, "scale"),
        clientWidth=_get_number(viewport, "clientWidth"),
        clientHeight=_get_number(viewport, "clientHeight"),
        scrollWidth=_get_number(viewport, "scrollWidth"),
        scrollHeight=_get_number(viewport, "scrollHeight"),
    )


def add_set_of_mark(
    screenshot: bytes | Image.Image | io.BufferedIOBase,
    ROIs: Dict[str, InteractiveRegion],
) -> Tuple[Image.Image, List[str], List[str], List[str]]:
    if isinstance(screenshot, Image.Image):
        return _add_set_of_mark(screenshot, ROIs)

    if isinstance(screenshot, bytes):
        screenshot = io.BytesIO(screenshot)

    image = Image.open(cast(BinaryIO, screenshot))
    comp, visible_rects, rects_above, rects_below = _add_set_of_mark(
        image, ROIs
    )
    image.close()
    return comp, visible_rects, rects_above, rects_below


def _add_set_of_mark(
    screenshot: Image.Image, ROIs: Dict[str, InteractiveRegion]
) -> Tuple[Image.Image, List[str], List[str], List[str]]:
    visible_rects: List[str] = list()
    rects_above: List[str] = list()  # Scroll up to see
    rects_below: List[str] = list()  # Scroll down to see

    fnt = ImageFont.load_default(14)
    base = screenshot.convert("L").convert("RGBA")
    overlay = Image.new("RGBA", base.size)

    draw = ImageDraw.Draw(overlay)
    for r in ROIs:
        for rect in ROIs[r]["rects"]:
            # Empty rectangles
            if not rect:
                continue
            if rect["width"] * rect["height"] == 0:
                continue

            mid = (
                (rect["right"] + rect["left"]) / 2.0,
                (rect["top"] + rect["bottom"]) / 2.0,
            )

            if 0 <= mid[0] and mid[0] < base.size[0]:
                if mid[1] < 0:
                    rects_above.append(r)
                elif mid[1] >= base.size[1]:
                    rects_below.append(r)
                else:
                    visible_rects.append(r)
                    _draw_roi(draw, int(r), fnt, rect)

    comp = Image.alpha_composite(base, overlay)
    overlay.close()
    return comp, visible_rects, rects_above, rects_below


def _draw_roi(
    draw: ImageDraw.ImageDraw,
    idx: int,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    rect: DOMRectangle,
) -> None:
    color = _color(idx)
    luminance = color[0] * 0.3 + color[1] * 0.59 + color[2] * 0.11
    text_color = (0, 0, 0, 255) if luminance > 90 else (255, 255, 255, 255)

    roi = ((rect["left"], rect["top"]), (rect["right"], rect["bottom"]))

    label_location = (rect["right"], rect["top"])
    label_anchor = "rb"

    if label_location[1] <= TOP_NO_LABEL_ZONE:
        label_location = (rect["right"], rect["bottom"])
        label_anchor = "rt"

    draw.rectangle(
        roi, outline=color, fill=(color[0], color[1], color[2], 48), width=2
    )

    bbox = draw.textbbox(
        label_location,
        str(idx),
        font=font,
        anchor=label_anchor,
        align="center",
    )
    bbox = (bbox[0] - 3, bbox[1] - 3, bbox[2] + 3, bbox[3] + 3)
    draw.rectangle(bbox, fill=color)

    draw.text(
        label_location,
        str(idx),
        fill=text_color,
        font=font,
        anchor=label_anchor,
        align="center",
    )


def _color(identifier: int) -> Tuple[int, int, int, int]:
    rnd = random.Random(int(identifier))
    color = [rnd.randint(0, 255), rnd.randint(125, 255), rnd.randint(0, 50)]
    rnd.shuffle(color)
    color.append(255)
    return cast(Tuple[int, int, int, int], tuple(color))


class BaseBrowser:
    def __init__(self, headless=True, cache_dir: Optional[str] = None):
        r"""Initialize the WebBrowserToolkit instance.

        Args:
            headless (bool): Whether to run the browser in headless mode.
            cache_dir (Union[str, None]): The directory to store cache files.

        Returns:
            None
        """
        from playwright.sync_api import (
            sync_playwright,
        )

        self.history: list = []
        self.headless = headless
        self.playwright = sync_playwright().start()
        self.page_history: list = []  # stores the history of visited pages

        # set the cache directory
        self.cache_dir = "tmp/"
        os.makedirs(self.cache_dir, exist_ok=True)
        if cache_dir is not None:
            self.cache_dir = cache_dir

        # load the page script
        abs_dir_path = os.path.dirname(os.path.abspath(__file__))
        page_script_path = os.path.join(abs_dir_path, "page_script.js")

        try:
            with open(page_script_path, "r", encoding='utf-8') as f:
                self.page_script = f.read()
            f.close()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Page script file not found at path: {page_script_path}"
            )

    def init(self):
        r"""Initialize the browser."""
        self.browser = self.playwright.chromium.launch(
            headless=self.headless
        )  # Launch the browser, if headless is False, the browser will display
        self.context = self.browser.new_context(
            accept_downloads=True
        )  # create a new context
        self.page = self.context.new_page()  # create a new page

    def clean_cache(self):
        r"""delete the cache directory and its contents."""
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

    def _wait_for_load(self, timeout: int = 20):
        r"""Wait for a certain amount of time for the page to load."""
        timeout_ms = timeout * 1000

        self.page.wait_for_load_state("load", timeout=timeout_ms)
        time.sleep(2)

    def click_blank_area(self):
        r"""Click a blank area of the page to unfocus the current element."""
        self.page.mouse.click(0, 0)
        self._wait_for_load()

    def visit_page(self, url: str):
        r"""Visit a page with the given URL."""

        self.page.goto(url)
        self._wait_for_load()
        self.page_url = url

    def ask_question_about_video(self, question: str) -> str:
        r"""Ask a question about the video on the current page. It is suitable
        to process youtube video.

        Args:
            question (str): The question to ask.

        Returns:
            str: The answer to the question.
        """
        video_analyzer = VideoAnalysisToolkit()
        result = video_analyzer.ask_question_about_video(
            self.page_url, question
        )
        return result

    @retry_on_error()
    def get_screenshot(
        self, save_image: bool = False
    ) -> Tuple[Image.Image, Union[str, None]]:
        r"""Get a screenshot of the current page.

        Args:
            save_image (bool): Whether to save the image to the cache
                directory.

        Returns:
            Tuple[Image.Image, str]: A tuple containing the screenshot image
                and the path to the image file.
        """

        image_data = self.page.screenshot(timeout=60000)
        image = Image.open(io.BytesIO(image_data))

        file_path = None
        if save_image:
            # get url name to form a file name
            url_name = self.page_url.split("/")[-1]
            for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.']:
                url_name = url_name.replace(char, "_")

            # get formatted time: mmddhhmmss
            timestamp = datetime.datetime.now().strftime("%m%d%H%M%S")
            file_path = os.path.join(
                self.cache_dir, f"{url_name}_{timestamp}.png"
            )
            with open(file_path, "wb") as f:
                image.save(f, "PNG")
            f.close()

        return image, file_path

    def capture_full_page_screenshots(
        self, scroll_ratio: float = 0.8
    ) -> List[str]:
        r"""Capture full page screenshots by scrolling the page with a buffer
        zone.

        Args:
            scroll_ratio (float): The ratio of viewport height to scroll each
                step (default: 0.7).

        Returns:
            List[str]: A list of paths to the screenshot files.
        """
        screenshots = []
        scroll_height = self.page.evaluate("document.body.scrollHeight")
        viewport_height = self.page.viewport_size["height"]
        current_scroll = 0
        screenshot_index = 1

        url_name = self.page.url.split("/")[-1].replace(".", "_")
        timestamp = datetime.datetime.now().strftime("%m%d%H%M%S")
        base_file_path = os.path.join(
            self.cache_dir, f"{url_name}_{timestamp}"
        )

        max_height = scroll_height - viewport_height
        scroll_step = int(viewport_height * scroll_ratio)

        last_height = 0

        while True:
            logger.debug(
                f"Current scroll: {current_scroll}, max_height: "
                f"{max_height}, step: {scroll_step}"
            )

            file_path = f"{base_file_path}_{screenshot_index}.png"
            _, file_path = self.get_screenshot(save_image=True)
            screenshots.append(file_path)

            self.page.evaluate(f"window.scrollBy(0, {scroll_step})")
            time.sleep(0.5)

            current_scroll = self.page.evaluate("window.scrollY")
            if abs(current_scroll - last_height) < viewport_height * 0.1:
                break

            last_height = current_scroll
            screenshot_index += 1

        return screenshots

    def get_visual_viewport(self) -> VisualViewport:
        r"""Get the visual viewport of the current page.

        Returns:
            VisualViewport: The visual viewport of the current page.
        """
        try:
            self.page.evaluate(self.page_script)
        except Exception as e:
            logger.warning(f"Error evaluating page script: {e}")

        return visualviewport_from_dict(
            self.page.evaluate("MultimodalWebSurfer.getVisualViewport();")
        )

    def get_interactive_elements(self) -> List[Dict[str, Any]]:
        # codes from magentic-one
        try:
            self.page.evaluate(self.page_script)
        except Exception as e:
            logger.warning(f"Error evaluating page script: {e}")

        result = cast(
            Dict[str, Dict[str, Any]],
            self.page.evaluate("MultimodalWebSurfer.getInteractiveRects();"),
        )

        typed_results: Dict[str, InteractiveRegion] = {}
        for k in result:
            typed_results[k] = interactiveregion_from_dict(result[k])

        return typed_results  # type: ignore[return-value]

    def get_som_screenshot(
        self, save_image: bool = False
    ) -> Tuple[Image.Image, Union[str, None]]:
        r"""Get a screenshot of the current viewport with interactive elements
        marked.

        Args:
            save_image (bool): Whether to save the image to the cache
                directory.

        Returns:
            Tuple[Image.Image, str]: A tuple containing the screenshot image
                and the path to the image file.
        """

        self._wait_for_load()
        screenshot, _ = self.get_screenshot(save_image=False)
        rects = self.get_interactive_elements()

        file_path = None
        comp, visible_rects, rects_above, rects_below = add_set_of_mark(
            screenshot,
            rects,  # type: ignore[arg-type]
        )
        if save_image:
            url_name = self.page_url.split("/")[-1]
            for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.']:
                url_name = url_name.replace(char, "_")
            timestamp = datetime.datetime.now().strftime("%m%d%H%M%S")
            file_path = os.path.join(
                self.cache_dir, f"{url_name}_{timestamp}.png"
            )
            with open(file_path, "wb") as f:
                comp.save(f, "PNG")
            f.close()

        return comp, file_path

    def scroll_up(self) -> None:
        self.page.keyboard.press("PageUp")

    def scroll_down(self) -> None:
        self.page.keyboard.press("PageDown")

    def get_url(self) -> str:
        return self.page.url

    def click_id(self, identifier: Union[str, int]):
        if isinstance(identifier, int):
            identifier = str(identifier)
        target = self.page.locator(f"[__elementId='{identifier}']")

        try:
            target.wait_for(timeout=5000)
        except (TimeoutError, Exception) as e:
            logger.debug(f"Error during click operation: {e}")
            raise ValueError("No such element.") from None

        target.scroll_into_view_if_needed()

        new_page = None
        try:
            with self.page.expect_event("popup", timeout=1000) as page_info:
                box = cast(Dict[str, Union[int, float]], target.bounding_box())
                self.page.mouse.click(
                    box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                )
                new_page = page_info.value

                # If a new page is opened, switch to it
                if new_page:
                    self.page_history.append(deepcopy(self.page.url))
                    self.page = new_page

        except (TimeoutError, Exception) as e:
            logger.debug(f"Error during click operation: {e}")
            pass

        self._wait_for_load()

    def extract_url_content(self):
        r"""Extract the content of the current page."""
        content = self.page.content()
        return content

    def download_file_id(self, identifier: Union[str, int]) -> str:
        r"""Download a file with the given selector.

        Args:
            identifier (str): The identifier of the file to download.
            file_path (str): The path to save the downloaded file.

        Returns:
            str: The result of the action.
        """

        if isinstance(identifier, int):
            identifier = str(identifier)
        try:
            target = self.page.locator(f"[__elementId='{identifier}']")
        except (TimeoutError, Exception) as e:
            logger.debug(f"Error during download operation: {e}")
            logger.warning(
                f"Element with identifier '{identifier}' not found."
            )
            return f"Element with identifier '{identifier}' not found."

        target.scroll_into_view_if_needed()

        file_path = os.path.join(self.cache_dir)
        self._wait_for_load()

        try:
            with self.page.expect_download() as download_info:
                target.click()
                download = download_info.value
                file_name = download.suggested_filename

                file_path = os.path.join(file_path, file_name)
                download.save_as(file_path)

            return f"Downloaded file to path '{file_path}'."

        except (TimeoutError, Exception) as e:
            logger.debug(f"Error during download operation: {e}")
            return f"Failed to download file with identifier '{identifier}'."

    def fill_input_id(self, identifier: Union[str, int], text: str) -> str:
        r"""Fill an input field with the given text, and then press Enter.

        Args:
            identifier (str): The identifier of the input field.
            text (str): The text to fill.

        Returns:
            str: The result of the action.
        """
        if isinstance(identifier, int):
            identifier = str(identifier)

        try:
            target = self.page.locator(f"[__elementId='{identifier}']")
        except (TimeoutError, Exception) as e:
            logger.debug(f"Error during fill operation: {e}")
            logger.warning(
                f"Element with identifier '{identifier}' not found."
            )
            return f"Element with identifier '{identifier}' not found."

        target.scroll_into_view_if_needed()
        target.focus()
        try:
            target.fill(text)
        except (TimeoutError, Exception) as e:
            logger.debug(f"Error during fill operation: {e}")
            target.press_sequentially(text)

        target.press("Enter")
        self._wait_for_load()
        return (
            f"Filled input field '{identifier}' with text '{text}' "
            f"and pressed Enter."
        )

    def scroll_to_bottom(self) -> str:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        self._wait_for_load()
        return "Scrolled to the bottom of the page."

    def scroll_to_top(self) -> str:
        self.page.evaluate("window.scrollTo(0, 0);")
        self._wait_for_load()
        return "Scrolled to the top of the page."

    def hover_id(self, identifier: Union[str, int]) -> str:
        r"""Hover over an element with the given identifier.

        Args:
            identifier (str): The identifier of the element to hover over.

        Returns:
            str: The result of the action.
        """
        if isinstance(identifier, int):
            identifier = str(identifier)
        try:
            target = self.page.locator(f"[__elementId='{identifier}']")
        except (TimeoutError, Exception) as e:
            logger.debug(f"Error during hover operation: {e}")
            logger.warning(
                f"Element with identifier '{identifier}' not found."
            )
            return f"Element with identifier '{identifier}' not found."

        target.scroll_into_view_if_needed()
        target.hover()
        self._wait_for_load()
        return f"Hovered over element with identifier '{identifier}'."

    def find_text_on_page(self, search_text: str) -> str:
        r"""Find the next given text on the page, and scroll the page to the
        targeted text. It is equivalent to pressing Ctrl + F and searching for
        the text.
        """
        # ruff: noqa: E501
        script = f"""
        (function() {{
            let text = "{search_text}";
            let found = window.find(text);
            if (!found) {{
                let elements = document.querySelectorAll("*:not(script):not(style)"); 
                for (let el of elements) {{
                    if (el.innerText && el.innerText.includes(text)) {{
                        el.scrollIntoView({{behavior: "smooth", block: "center"}});
                        el.style.backgroundColor = "yellow";
                        el.style.border = '2px solid red';
                        return true;
                    }}
                }}
                return false;
            }}
            return true;
        }})();
        """
        found = self.page.evaluate(script)
        self._wait_for_load()
        if found:
            return f"Found text '{search_text}' on the page."
        else:
            return f"Text '{search_text}' not found on the page."

    def back(self):
        r"""Navigate back to the previous page."""

        page_url_before = self.page.url
        self.page.go_back()

        page_url_after = self.page.url

        if page_url_after == "about:blank":
            self.visit_page(page_url_before)

        if page_url_before == page_url_after:
            # If the page is not changed, try to use the history
            if len(self.page_history) > 0:
                self.visit_page(self.page_history.pop())

        time.sleep(1)
        self._wait_for_load()

    def close(self):
        self.browser.close()
        self.playwright.stop()

    # ruff: noqa: E501
    def show_interactive_elements(self):
        r"""Show simple interactive elements on the current page."""
        self.page.evaluate(self.page_script)
        self.page.evaluate("""
        () => {
            document.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"]), [contenteditable="true"]').forEach(el => {
                el.style.border = '2px solid red';
            });
            }
        """)

    @retry_on_error()
    def get_webpage_content(self) -> str:
        from html2text import html2text

        self._wait_for_load()
        html_content = self.page.content()

        markdown_content = html2text(html_content)
        return markdown_content


class WebToolkit(BaseToolkit):
    r"""A class for browsing the web and interacting with web pages.

    This class provides methods for browsing the web and interacting with web
    pages.
    """

    def __init__(
        self,
        headless: bool = False,
        cache_dir: Optional[str] = None,
        history_window: int = 5,
        web_agent_model: Optional[BaseModelBackend] = None,
        planning_agent_model: Optional[BaseModelBackend] = None,
        output_language: str = "en",
    ):
        r"""Initialize the WebToolkit instance.

        Args:
            headless (bool): Whether to run the browser in headless mode.
            cache_dir (Union[str, None]): The directory to store cache files.
            history_window (int): The window size for storing the history of
                actions.
            web_agent_model (Optional[BaseModelBackend]): The model backend
                for the web agent.
            planning_agent_model (Optional[BaseModelBackend]): The model
                backend for the planning agent.
        """

        self.browser = BaseBrowser(headless=headless, cache_dir=cache_dir)

        self.history_window = history_window
        self.web_agent_model = web_agent_model
        self.planning_agent_model = planning_agent_model
        self.output_language = output_language

        self.history: list = []
        self.web_agent, self.planning_agent = self._initialize_agent()

    def _reset(self):
        self.web_agent.reset()
        self.planning_agent.reset()
        self.history = []
        os.makedirs(self.browser.cache_dir, exist_ok=True)

    def _initialize_agent(self) -> Tuple["ChatAgent", "ChatAgent"]:
        r"""Initialize the agent."""
        from camel.agents import ChatAgent

        if self.web_agent_model is None:
            web_agent_model = ModelFactory.create(
                model_platform=ModelPlatformType.OPENAI,
                model_type=ModelType.GPT_4O,
                model_config_dict={"temperature": 0, "top_p": 1},
            )
        else:
            web_agent_model = self.web_agent_model

        if self.planning_agent_model is None:
            planning_model = ModelFactory.create(
                model_platform=ModelPlatformType.OPENAI,
                model_type=ModelType.O3_MINI,
            )
        else:
            planning_model = self.planning_agent_model

        system_prompt = """
You are a helpful web agent that can assist users in browsing the web.
Given a high-level task, you can leverage predefined browser tools to help 
users achieve their goals.
        """

        web_agent = ChatAgent(
            system_message=system_prompt,
            model=web_agent_model,
            output_language=self.output_language,
        )

        planning_system_prompt = """
You are a helpful planning agent that can assist users in planning complex 
tasks which need multi-step browser interaction.
        """

        planning_agent = ChatAgent(
            system_message=planning_system_prompt,
            model=planning_model,
            output_language=self.output_language,
        )

        return web_agent, planning_agent

    def _observe(
        self, task_prompt: str, detailed_plan: Optional[str] = None
    ) -> Tuple[str, str, str]:
        r"""Let agent observe the current environment, and get the next action."""

        detailed_plan_prompt = ""

        if detailed_plan is not None:
            detailed_plan_prompt = f"""
Here is a plan about how to solve the task step-by-step which you must follow: 
<detailed_plan>{detailed_plan}<detailed_plan>
        """

        observe_prompt = f"""
Please act as a web agent to help me complete the following high-level task: 
<task>{task_prompt}</task>
Now, I have made screenshot (only the current viewport, not the full webpage) 
based on the current browser state, and marked interactive elements in the 
webpage.
Please carefully examine the requirements of the task, and current state of 
the browser, and provide the next appropriate action to take.

{detailed_plan_prompt}

Here are the current available browser functions you can use:
{AVAILABLE_ACTIONS_PROMPT}

Here are the latest {self.history_window} trajectory (at most) you have taken:
<history>
{self.history[-self.history_window:]}
</history>

Your output should be in json format, including the following fields:
- `observation`: The detailed image description about the current viewport. Do 
not over-confident about the correctness of the history actions. You should 
always check the current viewport to make sure the correctness of the next 
action.
- `reasoning`: The reasoning about the next action you want to take, and the 
possible obstacles you may encounter, and how to solve them. Do not forget to 
check the history actions to avoid the same mistakes.
- `action_code`: The action code you want to take. It is only one step action 
code, without any other texts (such as annotation)

Here are an example of the output:
```json
{{
    "observation": [IMAGE_DESCRIPTION],
    "reasoning": [YOUR_REASONING],
    "action_code": "fill_input_id([ID], [TEXT])"
}}

Here are some tips for you:
- Never forget the overall question: **{task_prompt}**
- Maybe after a certain operation (e.g. click_id), the page content has not 
changed. You can check whether the action step is successful by looking at the 
`success` of the action step in the history. If successful, it means that the 
page content is indeed the same after the click. You need to try other methods.
- If using one way to solve the problem is not successful, try other ways. 
Make sure your provided ID is correct!
- Some cases are very complex and need to be achieve by an iterative process. 
You can use the `back()` function to go back to the previous page to try other 
methods.
- There are many links on the page, which may be useful for solving the 
problem. You can use the `click_id()` function to click on the link to see if 
it is useful.
- Always keep in mind that your action must be based on the ID shown in the 
current image or viewport, not the ID shown in the history.
- Do not use `stop()` lightly. Always remind yourself that the image only 
shows a part of the full page. If you cannot find the answer, try to use 
functions like `scroll_up()` and `scroll_down()` to check the full content of 
the webpage before doing anything else, because the answer or next key step 
may be hidden in the content below.
- If the webpage needs human verification, you must avoid processing it. 
Please use `back()` to go back to the previous page, and try other ways.
- If you have tried everything and still cannot resolve the issue, please stop 
the simulation, and report issues you have encountered.
- Check the history actions carefully, detect whether you have repeatedly made 
the same actions or not.
- When dealing with wikipedia revision history related tasks, you need to 
think about the solution flexibly. First, adjust the browsing history 
displayed on a single page to the maximum, and then make use of the 
find_text_on_page function. This is extremely useful which can quickly locate 
the text you want to find and skip massive amount of useless information.
- Flexibly use interactive elements like slide down selection bar to filter 
out the information you need. Sometimes they are extremely useful.
```
        """

        # get current state
        som_screenshot, som_screenshot_path = self.browser.get_som_screenshot(
            save_image=True
        )
        img = _reload_image(som_screenshot)
        message = BaseMessage.make_user_message(
            role_name='user', content=observe_prompt, image_list=[img]
        )
        resp = self.web_agent.step(message)

        resp_content = resp.msgs[0].content

        resp_dict = _parse_json_output(resp_content)
        observation_result: str = resp_dict.get("observation", "")
        reasoning_result: str = resp_dict.get("reasoning", "")
        action_code: str = resp_dict.get("action_code", "")

        if action_code and "(" in action_code and ")" not in action_code:
            action_match = re.search(
                r'"action_code"\s*:\s*[`"]([^`"]*\([^)]*\))[`"]', resp_content
            )
            if action_match:
                action_code = action_match.group(1)
            else:
                logger.warning(
                    f"Incomplete action_code detected: {action_code}"
                )
                if action_code.startswith("fill_input_id("):
                    parts = action_code.split(",", 1)
                    if len(parts) > 1:
                        id_part = (
                            parts[0].replace("fill_input_id(", "").strip()
                        )
                        action_code = f"fill_input_id({id_part}, 'Please fill the text here.')"

        action_code = action_code.replace("`", "").strip()

        return observation_result, reasoning_result, action_code

    def _act(self, action_code: str) -> Tuple[bool, str]:
        r"""Let agent act based on the given action code.
        Args:
            action_code (str): The action code to act.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating whether
                the action was successful, and the information to be returned.
        """

        def _check_if_with_feedback(action_code: str) -> bool:
            r"""Check if the action code needs feedback."""

            for action_with_feedback in ACTION_WITH_FEEDBACK_LIST:
                if action_with_feedback in action_code:
                    return True

            return False

        prefix = "self.browser."
        code = f"{prefix}{action_code}"

        try:
            if _check_if_with_feedback(action_code):
                # execute code, and get the executed result
                result = eval(code)
                time.sleep(1)
                return True, result

            else:
                exec(code)
                time.sleep(1)
                return True, "Action was successful."

        except Exception as e:
            time.sleep(1)
            return (
                False,
                f"Error while executing the action {action_code}: {e}. "
                f"If timeout, please recheck whether you have provided the "
                f"correct identifier.",
            )

    def _get_final_answer(self, task_prompt: str) -> str:
        r"""Get the final answer based on the task prompt and current browser state.
        It is used when the agent thinks that the task can be completed without any further action, and answer can be directly found in the current viewport.
        """

        prompt = f"""
We are solving a complex web task which needs multi-step browser interaction. After the multi-step observation, reasoning and acting with web browser, we think that the task is currently solved.
Here are all trajectory we have taken:
<history>{self.history}</history>
Please find the final answer, or give valuable insights and founds (e.g. if previous actions contain downloading files, your output should include the path of the downloaded file) about the overall task: <task>{task_prompt}</task>
        """

        message = BaseMessage.make_user_message(
            role_name='user',
            content=prompt,
        )

        resp = self.web_agent.step(message)
        return resp.msgs[0].content

    def _make_reflection(self, task_prompt: str) -> str:
        r"""Make a reflection about the current state and the task prompt."""

        reflection_prompt = f"""
Now we are working on a complex task that requires multi-step browser interaction. The task is: <task>{task_prompt}</task>
To achieve this goal, we have made a series of observations, reasonings, and actions. We have also made a reflection on previous states.

Here are the global available browser functions we can use:
{AVAILABLE_ACTIONS_PROMPT}

Here are the latest {self.history_window} trajectory (at most) we have taken:
<history>{self.history[-self.history_window:]}</history>

The image provided is the current state of the browser, where we have marked interactive elements. 
Please carefully examine the requirements of the task, and the current state of the browser, and then make reflections on the previous steps, thinking about whether they are helpful or not, and why, offering detailed feedback and suggestions for the next steps.
Your output should be in json format, including the following fields:
- `reflection`: The reflection about the previous steps, thinking about whether they are helpful or not, and why, offering detailed feedback.
- `suggestion`: The suggestion for the next steps, offering detailed suggestions, including the common solutions to the overall task based on the current state of the browser.
        """
        som_image, _ = self.browser.get_som_screenshot()
        img = _reload_image(som_image)

        message = BaseMessage.make_user_message(
            role_name='user', content=reflection_prompt, image_list=[img]
        )

        resp = self.web_agent.step(message)

        return resp.msgs[0].content

    def _task_planning(self, task_prompt: str, start_url: str) -> str:
        r"""Plan the task based on the given task prompt."""

        # Here are the available browser functions we can use: {AVAILABLE_ACTIONS_PROMPT}

        planning_prompt = f"""
<task>{task_prompt}</task>
According to the problem above, if we use browser interaction, what is the general process of the interaction after visiting the webpage `{start_url}`? 

Please note that it can be viewed as Partially Observable MDP. Do not over-confident about your plan.
Please first restate the task in detail, and then provide a detailed plan to solve the task.
"""
        # Here are some tips for you: Please note that we can only see a part of the full page because of the limited viewport after an action. Thus, do not forget to use methods like `scroll_up()` and `scroll_down()` to check the full content of the webpage, because the answer or next key step may be hidden in the content below.

        message = BaseMessage.make_user_message(
            role_name='user', content=planning_prompt
        )

        resp = self.planning_agent.step(message)
        return resp.msgs[0].content

    def _task_replanning(
        self, task_prompt: str, detailed_plan: str
    ) -> Tuple[bool, str]:
        r"""Replan the task based on the given task prompt.

        Args:
            task_prompt (str): The original task prompt.
            detailed_plan (str): The detailed plan to replan.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating whether the task needs to be replanned, and the replanned schema.
        """

        # Here are the available browser functions we can use: {AVAILABLE_ACTIONS_PROMPT}
        replanning_prompt = f"""
We are using browser interaction to solve a complex task which needs multi-step actions.
Here are the overall task:
<overall_task>{task_prompt}</overall_task>

In order to solve the task, we made a detailed plan previously. Here is the detailed plan:
<detailed plan>{detailed_plan}</detailed plan>

According to the task above, we have made a series of observations, reasonings, and actions. Here are the latest {self.history_window} trajectory (at most) we have taken:
<history>{self.history[-self.history_window:]}</history>

However, the task is not completed yet. As the task is partially observable, we may need to replan the task based on the current state of the browser if necessary.
Now please carefully examine the current task planning schema, and our history actions, and then judge whether the task needs to be fundamentally replanned. If so, please provide a detailed replanned schema (including the restated overall task).

Your output should be in json format, including the following fields:
- `if_need_replan`: bool, A boolean value indicating whether the task needs to be fundamentally replanned.
- `replanned_schema`: str, The replanned schema for the task, which should not be changed too much compared with the original one. If the task does not need to be replanned, the value should be an empty string. 
"""
        resp = self.planning_agent.step(replanning_prompt)
        resp_dict = _parse_json_output(resp.msgs[0].content)

        if_need_replan = resp_dict.get("if_need_replan", False)
        replanned_schema = resp_dict.get("replanned_schema", "")

        if if_need_replan:
            return True, replanned_schema
        else:
            return False, replanned_schema

    @dependencies_required("playwright")
    def browser_simulation(
        self, task_prompt: str, start_url: str, round_limit: int = 12
    ) -> str:
        r"""A powerful toolkit which can simulate the browser interaction to solve the task which needs multi-step actions.

        Args:
            task_prompt (str): The task prompt to solve.
            start_url (str): The start URL to visit.
            round_limit (int): The round limit to solve the task (default: 12).

        Returns:
            str: The simulation result to the task.
        """

        self._reset()
        task_completed = False
        detailed_plan = self._task_planning(task_prompt, start_url)
        logger.debug(f"Detailed plan: {detailed_plan}")

        self.browser.init()
        self.browser.visit_page(start_url)

        for i in range(round_limit):
            observation, reasoning, action_code = self._observe(
                task_prompt, detailed_plan
            )
            logger.debug(f"Observation: {observation}")
            logger.debug(f"Reasoning: {reasoning}")
            logger.debug(f"Action code: {action_code}")

            if "stop" in action_code:
                task_completed = True
                trajectory_info = {
                    "round": i,
                    "observation": observation,
                    "thought": reasoning,
                    "action": action_code,
                    "action_if_success": True,
                    "info": None,
                    "current_url": self.browser.get_url(),
                }
                self.history.append(trajectory_info)
                break

            else:
                success, info = self._act(action_code)
                if not success:
                    logger.warning(f"Error while executing the action: {info}")

                trajectory_info = {
                    "round": i,
                    "observation": observation,
                    "thought": reasoning,
                    "action": action_code,
                    "action_if_success": success,
                    "info": info,
                    "current_url": self.browser.get_url(),
                }
                self.history.append(trajectory_info)

                # replan the task if necessary
                if_need_replan, replanned_schema = self._task_replanning(
                    task_prompt, detailed_plan
                )
                if if_need_replan:
                    detailed_plan = replanned_schema
                    logger.debug(f"Replanned schema: {replanned_schema}")

        if not task_completed:
            simulation_result = f"""
                The task is not completed within the round limit. Please check the last round {self.history_window} information to see if there is any useful information:
                <history>{self.history[-self.history_window:]}</history>
            """

        else:
            simulation_result = self._get_final_answer(task_prompt)

        self.browser.close()
        return simulation_result

    def get_tools(self) -> List[FunctionTool]:
        return [FunctionTool(self.browser_simulation)]
