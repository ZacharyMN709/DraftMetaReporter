from game_metadata import FORMATS, SetMetadata

from data_fetching.FramedData import FramedData


class SetManager:
    def __init__(self, set_code):
        self.SET = set_code
        self.DATA = {f: FramedData(set_code, f) for f in FORMATS}
        self.SET_METADATA = SetMetadata.get_metadata(set_code)

    def check_for_updates(self):
        """Populates and updates all data properties, filling in missing data."""
        for format_name in FORMATS:
            self[format_name].check_for_updates()

    def reload_data(self):
        """Populates and updates all data properties, reloading all data."""
        for format_name in FORMATS:
            self[format_name].reload_data()

    @property
    def CARDS(self):
        """The list of cards in the set."""
        return self.SET_METADATA.CARD_LIST

    def __getitem__(self, item):
        return self.DATA[item]

    # These are here for convenience, as they're the most often used data.
    @property
    def BO1(self):
        """Premier Draft data."""
        return self['PremierDraft']

    @property
    def BO3(self):
        """Traditional Draft data."""
        return self['TradDraft']

    @property
    def QD(self):
        """Quick Draft data."""
        return self['QuickDraft']
