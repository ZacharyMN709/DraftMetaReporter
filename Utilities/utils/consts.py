from typing import Union

# Typing Consts
CARD_DATA = list[dict[str, Union[str, int, float]]]
META_DATA = list[dict[str, Union[str, int, bool]]]
WUBRG_CARD_DATA = dict[str, CARD_DATA]
