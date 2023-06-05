from core import wubrg
from core.game_metadata import Card, SetMetadata
from core.utilities import flatten_lists, weave_lists


def split_by_rarity(card_list: list[Card]) -> list[list[Card]]:
    def get_by_rarity(rarity: str) -> list[Card]:
        return [card for card in card_list if card.RARITY == rarity]
    return [get_by_rarity(char) for char in 'CURM']


def split_by_color(card_list: list[Card]) -> list[list[Card]]:
    def get_by_color(color: str) -> list[Card]:
        return sorted([card for card in card_list if card.CAST_IDENTITY == color], key=lambda x: x.CMC)
    temp = [get_by_color(color) for color in wubrg.GROUP_COLOR_COMBINATIONS]
    colorless_temp = temp[0]
    colorless = [x for x in colorless_temp if 'Land' not in x.TYPES]
    land = [x for x in colorless_temp if 'Land' in x.TYPES]
    return [land, colorless] + temp[1:]


def gen_set_review_chunks(card_list: list[Card]) -> tuple[list[Card], list[Card], list[Card], list[Card], list[Card]]:
    commons, uncommons, rares, mythics = split_by_rarity(card_list)
    common_sublists = split_by_color(commons)
    uncommon_sublists = split_by_color(uncommons)
    rare_sublists = split_by_color(rares + mythics)

    lands = flatten_lists([common_sublists[0], uncommon_sublists[0]])
    colorless = flatten_lists([common_sublists[1], uncommon_sublists[1]])
    single_colored = flatten_lists(weave_lists(common_sublists[2:7], uncommon_sublists[2:7]))
    signposts = flatten_lists(weave_lists(common_sublists[7:], uncommon_sublists[7:]))
    rares_and_mythics = flatten_lists(rare_sublists[2:7] + rare_sublists[0:2] + rare_sublists[7:])

    return signposts, colorless, lands, single_colored, rares_and_mythics


def order_for_set_review(card_list: list[Card]) -> list[Card]:
    signposts, colorless, lands, single_colored, rares_and_mythics = gen_set_review_chunks(card_list)
    return flatten_lists([signposts, colorless, lands, single_colored, rares_and_mythics])


def get_set_order(set_code: str) -> list[Card]:
    metadata = SetMetadata.get_metadata(set_code)
    card_list = metadata.CARD_LIST.copy()
    ordered = order_for_set_review(card_list)
    return ordered
