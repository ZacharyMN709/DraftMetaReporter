from io import BytesIO
from PIL import Image

import config as cfg
import caching


def format_image(card_image_url, rotate, out_loc):
    image_data = caching.get_image_data(card_image_url)

    with BytesIO(image_data) as b_io:
        with Image.open(b_io) as img:
            new_height = cfg.HEIGHT
            new_width = cfg.WIDTH

            if rotate:
                img = img.rotate(270, expand=True)  # Rotate image by -90 degrees
                new_height, new_width = new_width, new_height  # Switch the height and width, since we've rotated.

            # Save the image fetched from the web as a JPEG, then use that file location to add the image into the docx.
            img.save(out_loc, format='JPEG')
    return new_height, new_width


def download_card_image(card_name):
    def _get_url(face):
        uris = ['large', 'border_crop', 'normal', 'small', 'art_crop']
        for uri in uris:
            if uri in face["image_uris"]:
                return face["image_uris"][uri]

    card_data = caching.get_card_data(card_name)

    if "layout" in card_data and card_data["layout"] == "transform":
        front_face = card_data["card_faces"][0]
        rotate = front_face['type_line'] == 'Battle — Siege'
        height, width = format_image(_get_url(front_face), rotate, cfg.TEMP_FRONT_LOC)
        front = Image.open(cfg.TEMP_FRONT_LOC)

        back_face = card_data["card_faces"][1]
        h, w = format_image(_get_url(back_face), False, cfg.TEMP_BACK_LOC)
        height = max(height, h)
        width += w
        back = Image.open(cfg.TEMP_BACK_LOC)

        new = Image.new('RGBA', (front.size[0] + back.size[0], max(front.size[1], back.size[1])), (255, 255, 255, 255))
        new.paste(front, (0, (new.size[1] - front.size[1]) // 2))
        new.paste(back, (front.size[0], (new.size[1] - back.size[1]) // 2))
        new.save(cfg.TEMP_LOC, format='PNG')
    else:
        height, width = format_image(_get_url(card_data), False, cfg.TEMP_LOC)

    return height, width
