from pptx import Presentation as new_presentation
from pptx.slide import Slide
from pptx.util import Cm
from pptx.presentation import Presentation
from PIL import Image
import tempfile

SLIDE_HEIGHT = 19.05
SLIDE_WIDTH = 25.40


def add_image_slide(
        presentation: Presentation,
        image_path: str,
        left_margin: float = 2,
        top_margin: float = 2,
        height: float = None,
        width: float = None
):
    blank_slide_layout = presentation.slide_layouts[6]
    slide = presentation.slides.add_slide(blank_slide_layout)
    left = Cm(left_margin)
    top = Cm(top_margin)
    if height:
        height = Cm(height)
    if width:
        width = Cm(width)

    slide.shapes.add_picture(image_path, left, top, height=height, width=width)


def add_centered_image_slide(
        presentation: Presentation,
        img: Image,
        min_horizontal_margin: float = 2,
        min_vertical_margin: float = 2,
):
    width, height = img.size
    height_ratio = height / (SLIDE_HEIGHT - min_vertical_margin*2)
    width_ratio = width / (SLIDE_WIDTH - min_horizontal_margin*2)
    is_landscape = width_ratio >= height_ratio

    if is_landscape:
        height = height / width_ratio
        width = width / width_ratio
        horizontal_margin = min_horizontal_margin
        vertical_margin = (SLIDE_HEIGHT - height) / 2
    else:
        height = height / height_ratio
        width = width / height_ratio
        horizontal_margin = (SLIDE_WIDTH - width) / 2
        vertical_margin = min_vertical_margin


    tmp = tempfile.NamedTemporaryFile(suffix='.png')
    img.save(tmp)
    add_image_slide(presentation, tmp, horizontal_margin, vertical_margin, height, width)
