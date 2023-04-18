import caching
import tier_parsing
import document_processing


def create_document(card_names, doc_name="test.docx", hori_margin=3.18, vert_margin=2.54):
    document = document_processing.new_document(hori_margin=hori_margin, vert_margin=vert_margin)

    cnt = 0
    for card_name in card_names:
        card_name = card_name.strip()
        card_data = caching.get_card_data(card_name)

        if card_data:
            document_processing.add_card_to_document(document, card_name)
            cnt += 1
            if cnt % 2 == 0:
                document.add_page_break()

        else:
            print(f"Card not found: {card_name}")

    document.save(doc_name)


def main(card_list=None):
    if card_list is None:
        card_list = [card_name for card_name in tier_parsing.SET_GRADES.index]

    patched_cards = [caching.get_card_data(card_name)['name'] for card_name in card_list]
    create_document(patched_cards, "test_3.docx", 1.5, 1)


if __name__ == "__main__":
    test_order = [
        "Botanical Brawler",
        "Invasion of Moag",
        "Tarkir Duneshaper",
    ]

    main(test_order)
