from pptx import Presentation as new_presentation

from core.game_metadata import Card

import card_ordering
import caching
from utils import pptx_funcs

IMAGE_PATH = r"C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Notebooks\temp.jpeg"


def gen_powerpoint_half(cards: list[Card], file_name: str):
    prs = new_presentation()

    for card in cards:
        height, width = caching.download_card_image(card.NAME)
        pptx_funcs.add_centered_image_slide(prs, IMAGE_PATH)

    prs.save(file_name)


def gen_set_review_pptx(set_code: str, split_point: int):
    cards = card_ordering.get_set_order(set_code)

    commons_and_uncommons = cards[0:split_point]
    rares_and_mythic = cards[split_point:]

    gen_powerpoint_half(commons_and_uncommons,  f"{set_code} - Commons and Uncommons.pptx")
    gen_powerpoint_half(rares_and_mythic,  f"{set_code} - Rares and Mythics .pptx")


if __name__ == "__main__":
    SET = "LTR"
    SPLIT = 183

    gen_set_review_pptx(SET, SPLIT)
