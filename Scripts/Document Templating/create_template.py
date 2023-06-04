import caching
import tier_parsing
import document_processing
import config as cfg


def create_document(grades, card_names, doc_name="test.docx", hori_margin=3.18, vert_margin=2.54):
    doc_handler = document_processing.DocumentCreator(
        grades,
        left_margin=hori_margin,
        right_margin=hori_margin,
        top_margin=vert_margin,
        bottom_margin=vert_margin
    )

    for card_name in card_names:
        card_name = card_name.strip()
        card_data = caching.get_card_data(card_name)

        if card_data:
            doc_handler.add_card_to_document(card_name)
        else:
            print(f"Card not found: {card_name}")

    doc_handler.save_as(doc_name)


def main(set_grades, card_list=None):

    if card_list is None:
        card_list = [card_name for card_name in set_grades.index]

    patched_cards = [caching.get_card_data(card_name)['name'] for card_name in card_list]
    create_document(set_grades, patched_cards, "test_3.docx", 1.5, 1)


if __name__ == "__main__":
    set_grades = tier_parsing.parse_chord_excel(cfg.TIER_LIST_LOC, tier_parsing.patch_chord_excel)

    test_order = [
        "Botanical Brawler",
        "Invasion of Moag",
        "Tarkir Duneshaper",
    ]

    main(set_grades, test_order)
