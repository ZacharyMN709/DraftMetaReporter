from game_metadata import SETS, FORMATS, SetMetadata, Card

from data_fetching.FramedData import FramedData


# Gets lists of draft done by logged-in user.
# https://www.17lands.com/user/data?start_date=2019-01-01&end_date=2022-04-20

# Deck match information:
# https://www.17lands.com/data/details?draft_id=fdbe8fad413c4c84890760a985b8c5ef

# Deck List:
# https://www.17lands.com/data/deck?draft_id=fdbe8fad413c4c84890760a985b8c5ef&deck_index=0

# Deck card Pool:
# https://www.17lands.com/data/pool?draft_id=fdbe8fad413c4c84890760a985b8c5ef&deck_index=0

# Draft Picks Record:
# https://www.17lands.com/data/draft/stream?draft_id=fdbe8fad413c4c84890760a985b8c5ef


class SetManager:  # pragma: no cover
    """
    Acts as a wrapper for FramedData, mostly for convenience in loading multiple formats for one set under one object.
    """
    def __init__(self, set_code, load_summary: bool = True, load_history: bool = True):
        self.SET: str = set_code
        self.DATA: dict[str, FramedData] = {f: FramedData(set_code, f, load_summary, load_history) for f in FORMATS}
        self.load_summary: bool = load_summary
        self.load_history: bool = load_history
        self.SET_METADATA: SetMetadata = SetMetadata.get_metadata(set_code)

    def check_for_updates(self) -> None:
        """Populates and updates all data properties, filling in missing data."""
        for format_name in FORMATS:
            self[format_name].check_for_updates()

    def reload_data(self) -> None:
        """Populates and updates all data properties, reloading all data."""
        for format_name in FORMATS:
            self[format_name].reload_data()

    @property
    def CARDS(self) -> list[Card]:
        """The list of cards in the set."""
        return self.SET_METADATA.CARD_LIST

    def __getitem__(self, item) -> FramedData:
        return self.DATA[item]

    # These are here for convenience, as they're the most often used data.
    @property
    def BO1(self) -> FramedData:
        """Premier Draft data."""
        return self['PremierDraft']

    @property
    def BO3(self) -> FramedData:
        """Traditional Draft data."""
        return self['TradDraft']

    @property
    def QD(self) -> FramedData:
        """Quick Draft data."""
        return self['QuickDraft']


class CentralManager:  # pragma: no cover
    """
    Acts as a wrapper for SetManager, aggregating all possible data into one root object.
    """
    def __init__(self, load_summary: bool = True, load_history: bool = True):
        self.DATA: dict[str, SetManager] = {s: SetManager(s, load_summary, load_history) for s in SETS}
        self.load_summary: bool = load_summary
        self.load_history: bool = load_history

    def check_for_updates(self) -> None:
        """Populates and updates all data properties, filling in missing data."""
        for set_code in SETS:
            self[set_code].check_for_updates()

    def reload_data(self) -> None:
        """Populates and updates all data properties, reloading all data."""
        for set_code in SETS:
            self[set_code].reload_data()

    def __getitem__(self, item) -> SetManager:
        return self.DATA[item]

    # These are here for convenience, as they're the most often used data.
    @property
    def DMU(self) -> SetManager:
        return self.DATA['DMU']

    @property
    def SNC(self) -> SetManager:
        return self.DATA['SNC']

    @property
    def NEO(self) -> SetManager:
        return self.DATA['NEO']

