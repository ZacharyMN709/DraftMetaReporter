from game_metadata import SETS, FORMATS, SetMetadata

from data_fetching.FramedData import FramedData


class SetManager:
    """
    Acts as a wrapper for FramedData, mostly for convenience in loading multiple formats for one set under one object.
    """
    def __init__(self, set_code, load_summary: bool = True, load_history: bool = True):
        self.SET = set_code
        self.DATA = {f: FramedData(set_code, f, load_summary, load_history) for f in FORMATS}
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


class CentralManager:
    """
    Acts as a wrapper for SetManager, aggregating all possible data into one root object.
    """
    def __init__(self, load_summary: bool = True, load_history: bool = True):
        self.DATA = dict()
        self.load_summary = load_summary
        self.load_history = load_history

    def check_for_updates(self):
        """Populates and updates all data properties, filling in missing data."""
        for set_code in SETS:
            self[set_code].check_for_updates()

    def reload_data(self):
        """Populates and updates all data properties, reloading all data."""
        for set_code in SETS:
            self[set_code].reload_data()

    def __getitem__(self, item):
        return self.DATA[item]

    # These are here for convenience, as they're the most often used data.
    @property
    def NEO(self):
        if 'NEO' not in self.DATA:
            self.DATA['NEO'] = SetManager('NEO')
        return self.DATA['NEO']

    @property
    def SNC(self):
        if 'SNC' not in self.DATA:
            self.DATA['SNC'] = SetManager('SNC')
        return self.DATA['SNC']
