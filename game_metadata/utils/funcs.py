from wubrg import COLOR


def new_color_count_dict() -> dict[COLOR, int]:
    d: dict[COLOR, int] = {
        # TODO: Consider if this should be part of wubrg module.
        # TODO: Consider hybrid and phyrexian mana costs.
        "W": 0,
        "U": 0,
        "B": 0,
        "R": 0,
        "G": 0,
    }
    return d
