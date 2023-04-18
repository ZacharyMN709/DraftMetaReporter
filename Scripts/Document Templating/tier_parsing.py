import pandas as pd

import config as cfg
import caching


def repair_names(frame):
    """Repairs all card names in the `Card Name` column, using scryfall's fuzzy search."""
    name_patch = {card_name: caching.get_card_data(card_name)['name'] for card_name in frame["Card Name"]}
    frame = frame.replace({"Card Name": name_patch})
    return frame


def patch_chord_excel(frame):
    def fix_typos(frame):
        """Patches card names scryfall cannot parse"""
        misnamed = {
            'Halo Forger': 'Halo Forager',
            'Invastion of Xerex': "Invasion of Xerex",
            'Invastion of Amonkhet': "Invasion of Amonkhet",
            'Invasion of Ragatha': "Invasion of Regatha",
            'Ariel Boost': "Aerial Boost",
            'Sun-Blessed Gaurdian': "Sun-Blessed Guardian",
            'Etali, Primal Conquerer': "Etali, Primal Conqueror",
            'Radah, Colition Warlord': "Radha, Coalition Warlord",
            'Seizan the Pervert': "Seizan, Perverter of Truths",
            "Horobi, Death's Whisper": "Horobi, Death's Wail",
            "Tetsuko Umezawa": "Tetsuko Umezawa, Fugitive"
        }
        return frame.replace({"Card Name": misnamed})

    def split_land_cycle(frame):
        """Converts a blanket grade for tap lands into a grade per card."""
        # 38 	Tap Land Cycle 	C+ 	C+

        frame = frame.drop([38], axis=0)
        extra = {
            "Card Name":
                ['Bloodfell Caves',
                 'Blossoming Sands',
                 'Dismal Backwater',
                 'Jungle Hollow',
                 'Rugged Highlands',
                 'Scoured Barrens',
                 'Swiftwater Cliffs',
                 'Thornwood Falls',
                 'Tranquil Cove',
                 'Wind-Scarred Crag'],
            "Marc": ["C+"] * 10,
            "Alex": ["C+"] * 10,
        }
        xtra = pd.DataFrame(extra)
        return pd.concat([frame, xtra])

    def add_missing(frame):
        """Adds cards missing from the input file"""
        missing = {
            "Card Name": [
                "Keruga, the Macrosage",
                "Ezuri, Claw of Progress",
                "Captain Lannery Storm",
            ],
            "Marc": [
                "SB",
                "SB",
                "SB",
            ],
            "Alex": [
                "SB",
                "SB",
                "SB",
            ],
        }
        xtra = pd.DataFrame(missing)
        return pd.concat([frame, xtra])

    frame = fix_typos(frame)
    frame = split_land_cycle(frame)
    frame = add_missing(frame)

    return frame


def parse_chord_excel(file_path, patch_func=None):
    """Read the grade spreadsheet, and applies cleanup to it."""
    frame = pd.read_excel(file_path)
    frame = frame.dropna(axis=0, how='all')  # Drop the spacer rows.
    frame = frame.drop(["COLOR", "RARITY"], axis=1)  # Drop the card info, as its not needed.
    frame.columns = ['Card Name', 'Marc', 'Alex']  # Set the column names, for consistency between files.
    if patch_func is not None:  # If a patch function was provided, use it to apply a data patch.
        frame = patch_func(frame)
    frame = repair_names(frame)  # Use scryfall to standardize names, fixing typos.
    frame = frame.set_index('Card Name')  # Use the card names as indexes, creating something like a 'layered' dict.
    return frame


SET_GRADES = parse_chord_excel(cfg.TIER_LIST_LOC, patch_chord_excel)
