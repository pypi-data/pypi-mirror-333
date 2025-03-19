import io
import random
from typing import BinaryIO, Dict, List, Tuple, cast

from PIL import Image, ImageDraw, ImageFont

from ._types import DOMRectangle, InteractiveRegion

TOP_NO_LABEL_ZONE = 20  # Don't print any labels close the top of the page


def add_set_of_mark(
    screenshot: bytes | Image.Image | io.BufferedIOBase, ROIs: Dict[str, InteractiveRegion]
) -> Tuple[Image.Image, List[str], List[str], List[str]]:
    if isinstance(screenshot, Image.Image):
        return _add_set_of_mark(screenshot, ROIs)

    if isinstance(screenshot, bytes):
        screenshot = io.BytesIO(screenshot)

    # TODO: Not sure why this cast was needed, but by this point screenshot is a binary file-like object
    image = Image.open(cast(BinaryIO, screenshot))
    comp, visible_rects, rects_above, rects_below = _add_set_of_mark(image, ROIs)
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

            mid = ((rect["right"] + rect["left"]) / 2.0, (rect["top"] + rect["bottom"]) / 2.0)

            if 0 <= mid[0] and mid[0] < base.size[0]:
                if mid[1] < 0:
                    rects_above.append(r)
                elif mid[1] >= base.size[1]:
                    rects_below.append(r)
                else:
                    visible_rects.append(r)
                    if ROIs[r]["role"].startswith("region_"):
                        _draw_roi(draw, int(r), fnt, rect, dashed=True)
                    else:
                        _draw_roi(draw, int(r), fnt, rect)
    comp = Image.alpha_composite(base, overlay)
    overlay.close()
    return comp, visible_rects, rects_above, rects_below


def _draw_roi(
    draw: ImageDraw.ImageDraw, idx: int, font: ImageFont.FreeTypeFont | ImageFont.ImageFont, rect: DOMRectangle, dashed: bool = False
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

    if dashed:
        left, top = rect["left"], rect["top"]
        right, bottom = rect["right"], rect["bottom"]
        
        draw_dashed_line(draw, [(left, top), (right, top)], 10, 5, 'black', 2)  # Top
        draw_dashed_line(draw, [(right, top), (right, bottom)], 10, 5, 'black', 2)  # Right
        draw_dashed_line(draw, [(right, bottom), (left, bottom)], 10, 5, 'black', 2)  # Bottom
        draw_dashed_line(draw, [(left, bottom), (left, top)], 10, 5, 'black', 2)  # Left
    else:
        draw.rectangle(roi, outline=color, fill=(color[0], color[1], color[2], 48), width=2)

    # TODO: Having trouble with these types being partially Unknown.
    bbox = draw.textbbox(label_location, str(idx), font=font, anchor=label_anchor, align="center")  # type: ignore
    bbox = (bbox[0] - 3, bbox[1] - 3, bbox[2] + 3, bbox[3] + 3)
    draw.rectangle(bbox, fill=color)

    # TODO: Having trouble with these types being partially Unknown.
    draw.text(label_location, str(idx), fill=text_color, font=font, anchor=label_anchor, align="center")  # type: ignore


def _color(identifier: int) -> Tuple[int, int, int, int]:
    rnd = random.Random(int(identifier))
    color = [rnd.randint(0, 255), rnd.randint(125, 255), rnd.randint(0, 50)]
    rnd.shuffle(color)
    color.append(255)
    return cast(Tuple[int, int, int, int], tuple(color))

def draw_dashed_line(draw, xy, dash_length, gap_length, fill=None, width=0):
    for i in range(0, len(xy) - 1):
        x1, y1 = xy[i]
        x2, y2 = xy[i + 1]
        
        dx = x2 - x1
        dy = y2 - y1
        line_length = (dx**2 + dy**2)**0.5
        
        if line_length == 0:
            continue
        
        num_segments = int(line_length / (dash_length + gap_length))
        
        for j in range(num_segments):
            start_ratio = j * (dash_length + gap_length) / line_length
            end_ratio = start_ratio + dash_length / line_length
            
            segment_x1 = x1 + dx * start_ratio
            segment_y1 = y1 + dy * start_ratio
            segment_x2 = x1 + dx * end_ratio
            segment_y2 = y1 + dy * end_ratio
            
            draw.line((segment_x1, segment_y1, segment_x2, segment_y2), fill=fill, width=width)