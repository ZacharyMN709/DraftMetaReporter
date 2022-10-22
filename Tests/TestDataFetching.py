import unittest
from datetime import date, datetime
from os import path

from pandas import DataFrame

from wubrg import subset
from game_metadata import FormatMetadata
from data_fetching.utils.date_helper import utc_today, get_prev_17lands_update_time, get_next_17lands_update_time
from data_fetching.utils.pandafy import gen_card_frame, gen_meta_frame
from data_fetching.utils.index_slice_helper import get_name_slice, get_color_slice, _stringify_for_date_slice, \
    get_date_slice
from data_fetching.utils.frame_filter_helper import rarity_filter, cmc_filter, card_color_filter, cast_color_filter, \
    compose_filters

from data_fetching import DataLoader, LoadedData, DataFramer, FramedData

CARD_KEYS_REQ = ['seen_count', 'avg_seen', 'pick_count', 'avg_pick', 'game_count', 'win_rate',
                 'opening_hand_game_count', 'opening_hand_win_rate', 'drawn_game_count', 'drawn_win_rate',
                 'ever_drawn_game_count', 'ever_drawn_win_rate', 'never_drawn_game_count', 'never_drawn_win_rate',
                 'drawn_improvement_win_rate', 'name', 'color', 'rarity']
CARD_KEYS_EXTRA = ['sideboard_game_count', 'sideboard_win_rate', 'url', 'url_back']
CARD_KEYS = CARD_KEYS_REQ + CARD_KEYS_EXTRA

META_KEYS = ['is_summary', 'color_name', 'wins', 'games']

CARD_DATA = [
            {'seen_count': 1423,
             'avg_seen': 8.179901616303583,
             'pick_count': 123,
             'avg_pick': 12.227642276422765,
             'game_count': 19,
             'win_rate': 0.21052631578947367,
             'sideboard_game_count': 511,
             'sideboard_win_rate': 0.5518590998043053,
             'opening_hand_game_count': 4,
             'opening_hand_win_rate': 0.0,
             'drawn_game_count': 5,
             'drawn_win_rate': 0.4,
             'ever_drawn_game_count': 9,
             'ever_drawn_win_rate': 0.2222222222222222,
             'never_drawn_game_count': 10,
             'never_drawn_win_rate': 0.2,
             'drawn_improvement_win_rate': 0.0222222222222222,
             'name': 'Healing Grace',
             'color': 'W',
             'rarity': 'common',
             'url': 'https://c1.scryfall.com/file/scryfall-cards/border_crop/front/f/7/f7512d31-dc35-4046-a1ba-49b74239c329.jpg?1562745837',
             'url_back': ''},
            {'seen_count': 25,
             'avg_seen': 1.92,
             'pick_count': 17,
             'avg_pick': 2.0588235294117645,
             'game_count': 52,
             'win_rate': 0.5769230769230769,
             'sideboard_game_count': 28,
             'sideboard_win_rate': 0.4642857142857143,
             'opening_hand_game_count': 6,
             'opening_hand_win_rate': 0.8333333333333334,
             'drawn_game_count': 13,
             'drawn_win_rate': 0.7692307692307693,
             'ever_drawn_game_count': 19,
             'ever_drawn_win_rate': 0.7894736842105263,
             'never_drawn_game_count': 33,
             'never_drawn_win_rate': 0.45454545454545453,
             'drawn_improvement_win_rate': 0.3349282296650718,
             'name': 'History of Benalia',
             'color': 'W',
             'rarity': 'mythic',
             'url': 'https://c1.scryfall.com/file/scryfall-cards/border_crop/front/d/1/d134385d-b01c-41c7-bb2d-30722b44dc5a.jpg?1562743350',
             'url_back': ''}
]

META_DATA = [
            {'is_summary': True, 'color_name': 'Two-color', 'wins': 1142, 'games': 1967},
            {'is_summary': True, 'color_name': 'Two-color + Splash', 'wins': 395, 'games': 697},
            {'is_summary': False, 'color_name': 'Azorius (WU)', 'wins': 140, 'games': 242},
            {'is_summary': False, 'color_name': 'Dimir (UB)', 'wins': 97, 'games': 165},
            {'is_summary': False, 'color_name': 'Rakdos (BR)', 'wins': 59, 'games': 112},
            {'is_summary': False, 'color_name': 'Gruul (RG)', 'wins': 26, 'games': 60},
            {'is_summary': False, 'color_name': 'Selesnya (GW)', 'wins': 18, 'games': 32},
            {'is_summary': False, 'color_name': 'Orzhov (WB)', 'wins': 129, 'games': 232},
            {'is_summary': False, 'color_name': 'Golgari (BG)', 'wins': 135, 'games': 230},
            {'is_summary': False, 'color_name': 'Simic (GU)', 'wins': 92, 'games': 144},
            {'is_summary': False, 'color_name': 'Izzet (UR)', 'wins': 361, 'games': 608},
            {'is_summary': False, 'color_name': 'Boros (RW)', 'wins': 85, 'games': 142}
]


class TestUtils(unittest.TestCase):
    def test_date_helpers(self):
        self.assertIsInstance(utc_today(), date)
        self.assertIsInstance(get_prev_17lands_update_time(), datetime)
        self.assertIsInstance(get_next_17lands_update_time(), datetime)

    def test_gen_card_frame(self):
        card_frame = gen_card_frame(CARD_DATA)
        self.assertEqual(len(card_frame), 2)

        def compare_card_frame(row_name: str, seen: int, alsa: float, picked: int, ata: float, gp: int, gp_wr: float,
                               oh: int, oh_wr: float, gd: int, gd_wr: float, gih: int, gih_wr: float,
                               gnd: int, gnd_wr: float, iwd: float, color: str, rarity: str):
            print(f'Checking {row_name}')
            self.assertEqual(card_frame.loc[row_name]['# Seen'], seen)
            self.assertAlmostEqual(card_frame.loc[row_name]['ALSA'], alsa, delta=0.05)
            self.assertEqual(card_frame.loc[row_name]['# Picked'], picked)
            self.assertAlmostEqual(card_frame.loc[row_name]['ATA'], ata, delta=0.05)
            self.assertEqual(card_frame.loc[row_name]['# GP'], gp)
            self.assertAlmostEqual(card_frame.loc[row_name]['GP WR'], gp_wr, delta=0.05)
            self.assertEqual(card_frame.loc[row_name]['# OH'], oh)
            self.assertAlmostEqual(card_frame.loc[row_name]['OH WR'], oh_wr, delta=0.05)
            self.assertEqual(card_frame.loc[row_name]['# GD'], gd)
            self.assertAlmostEqual(card_frame.loc[row_name]['GD WR'], gd_wr, delta=0.05)
            self.assertEqual(card_frame.loc[row_name]['# GIH'], gih)
            self.assertAlmostEqual(card_frame.loc[row_name]['GIH WR'], gih_wr, delta=0.05)
            self.assertEqual(card_frame.loc[row_name]['# GND'], gnd)
            self.assertAlmostEqual(card_frame.loc[row_name]['GND WR'], gnd_wr, delta=0.05)
            self.assertAlmostEqual(card_frame.loc[row_name]['IWD'], iwd, delta=0.05)
            self.assertEqual(card_frame.loc[row_name]['Color'], color)
            self.assertEqual(card_frame.loc[row_name]['Rarity'], rarity)

        compare_card_frame('Healing Grace', 1423, 8.18, 123, 12.228,
                           19, 21.053, 4, 0.0, 5, 40.0, 9, 22.22, 10, 20.0, 2.22, 'W', 'C')
        compare_card_frame('History of Benalia', 25, 1.920, 17, 2.059,
                           52, 57.692, 6, 83.333, 13, 76.923, 19, 78.947, 33, 45.455, 33.493, 'W', 'M')

    def test_gen_card_frame_empty(self):
        frame = gen_card_frame(list())
        self.assertEqual(len(frame), 0)

    def test_gen_meta_frame(self):
        sum_frame, arc_frame = gen_meta_frame(META_DATA)
        self.assertEqual(len(sum_frame), 2)
        self.assertEqual(len(arc_frame), 10)

        def compare_summary_frame(row_name: str, games: int, wins: int, winrate: float, splash: bool):
            frame_slice = sum_frame.loc[row_name]
            test_slice = frame_slice[frame_slice['Splash'] == splash]
            self.assertEqual(test_slice['Games'][0], games)
            self.assertEqual(test_slice['Wins'][0], wins)
            self.assertAlmostEqual(test_slice['Win %'][0], winrate, delta=0.05)

        def compare_archetype_frame(row_name: str, games: int, wins: int, winrate: float, splash: bool):
            self.assertEqual(arc_frame.loc[row_name]['Games'], games)
            self.assertEqual(arc_frame.loc[row_name]['Wins'], wins)
            self.assertAlmostEqual(arc_frame.loc[row_name]['Win %'], winrate, delta=0.05)
            self.assertEqual(arc_frame.loc[row_name]['Splash'], splash)

        compare_summary_frame('Two-Color', 1967, 1142, 58.060, False)
        compare_summary_frame('Two-Color', 697, 395, 56.670060, True)

        compare_archetype_frame('UR', 608, 361, 59.380, False)

    def test_gen_meta_frame_empty(self):
        sum_frame, arc_frame = gen_meta_frame(list())
        self.assertEqual(len(sum_frame), 0)
        self.assertEqual(len(arc_frame), 0)

    def test_name_index_helpers(self):
        # Handle None
        self.assertEqual(get_name_slice(None), slice(None))

        # Handle string
        self.assertListEqual(get_name_slice('Mesa Unicorn'), ['Mesa Unicorn'])

        # Handle slices
        self.assertEqual(get_name_slice(slice(None)), slice(None))
        self.assertEqual(get_name_slice(slice('Mesa Unicorn', 'Celebrity Fencer')),
                         slice('Mesa Unicorn', 'Celebrity Fencer'))

        # Handle list
        self.assertListEqual(get_name_slice(['Mesa Unicorn', 'Deathbloom Thallid', 'Blink of an Eye']),
                             ['Mesa Unicorn', 'Deathbloom Thallid', 'Blink of an Eye'])

        # Handle range
        self.assertEqual(get_name_slice(('Mesa Unicorn', 'Deathbloom Thallid')),
                         slice('Mesa Unicorn', 'Deathbloom Thallid'))

        # Handle invalid
        self.assertRaises(TypeError, get_name_slice, {'Mesa Unicorn'})
        self.assertRaises(TypeError, get_name_slice, {'Mesa Unicorn': ''})
        self.assertRaises(TypeError, get_name_slice, ('Mesa Unicorn', 'Deathbloom Thallid', 'Blink of an Eye'))

    def test_color_index_helpers(self):
        # Check Nones
        self.assertEqual(get_color_slice(None), slice(None))

        # Check string
        self.assertListEqual(get_color_slice('WU'), ['WU'])
        self.assertListEqual(get_color_slice('UW'), ['WU'])

        # Check slices
        self.assertEqual(get_color_slice(slice(None)), slice(None))
        self.assertEqual(get_color_slice(slice('', 'G')), slice('', 'G'))
        self.assertEqual(get_color_slice(slice('WU', 'RG')), slice('WU', 'RG'))

        # Handle lists
        self.assertListEqual(get_color_slice(['WU', 'WB']), ['WU', 'WB'])
        self.assertListEqual(get_color_slice(['WU', 'BW']), ['WU', 'WB'])
        self.assertListEqual(get_color_slice(['WU', 'WB', 'WR', 'WG']), ['WU', 'WB', 'WR', 'WG'])
        self.assertListEqual(get_color_slice(['UW', 'BW', 'RW', 'GW']), ['WU', 'WB', 'WR', 'WG'])
        self.assertListEqual(get_color_slice(['UW', 'BW', 'RW', 'GW', 'WG']), ['WU', 'WB', 'WR', 'WG', 'WG'])

        # Handle ranges
        self.assertEqual(get_color_slice(('', 'G')), slice('', 'G'))
        self.assertEqual(get_color_slice(('WU', 'RG')), slice('WU', 'RG'))
        self.assertEqual(get_color_slice(('RG', 'WU')), slice('RG', 'WU'))
        self.assertEqual(get_color_slice(('RG', 'UW')), slice('RG', 'WU'))

        # Handle invalid
        self.assertRaises(TypeError, get_color_slice, ('WU',))
        self.assertRaises(TypeError, get_color_slice, {'WU': '', 'WB': '', 'WR': '', 'WG': ''})
        self.assertRaises(TypeError, get_color_slice, ('WU', 'WB', 'WR', 'WG'))

    def test_date_index_helpers(self):
        # Check Date Stringifier
        self.assertEqual(_stringify_for_date_slice('2022-05-09'), '2022-05-09')
        self.assertEqual(_stringify_for_date_slice(date(2022, 5, 9)), '2022-05-09')
        self.assertEqual(_stringify_for_date_slice(datetime(2022, 5, 9, 5, 6)), '2022-05-09')
        self.assertRaises(TypeError, _stringify_for_date_slice, None)
        self.assertRaises(TypeError, _stringify_for_date_slice, True)

        # Check Nones
        self.assertEqual(get_date_slice(None), slice(None))

        # Check String and Dates
        self.assertListEqual(get_date_slice('2022-05-09'), ['2022-05-09'])
        self.assertListEqual(get_date_slice(date(2022, 5, 9)), ['2022-05-09'])
        self.assertListEqual(get_date_slice(datetime(2022, 5, 9, 5, 6)), ['2022-05-09'])

        # Check slices
        self.assertEqual(get_date_slice(slice('2022-05-09')), slice('2022-05-09'))
        self.assertEqual(get_date_slice(slice('2022-05-09', '2022-05-19')), slice('2022-05-09', '2022-05-19'))

        # Handle lists
        self.assertListEqual(get_date_slice(['2022-05-09', '2022-05-10', '2022-05-11', '2022-05-12']),
                             ['2022-05-09', '2022-05-10', '2022-05-11', '2022-05-12'])
        self.assertListEqual(get_date_slice(['2022-05-10', '2022-05-11', '2022-05-12', '2022-05-09']),
                             ['2022-05-10', '2022-05-11', '2022-05-12', '2022-05-09'])
        self.assertListEqual(get_date_slice(['2022-05-09', '2022-05-10', '2022-05-11', '2022-05-12', '2022-05-09']),
                             ['2022-05-09', '2022-05-10', '2022-05-11', '2022-05-12', '2022-05-09'])

        # Handle ranges
        self.assertEqual(get_date_slice(('2022-05-19', '2022-05-09')), slice('2022-05-19', '2022-05-09'))
        self.assertEqual(get_date_slice(('2022-05-09', '2022-05-19')), slice('2022-05-09', '2022-05-19'))

        # Handle invalid
        self.assertRaises(TypeError, get_date_slice, {'2022-05-10', '2022-05-11', '2022-05-12', '2022-05-09'})
        self.assertRaises(TypeError, get_date_slice, ('2022-05-09',))
        self.assertRaises(TypeError, get_date_slice, {'2022-05-09': '', '2022-05-10': '', '2022-05-11': '', '2022-05-12': ''})
        self.assertRaises(TypeError, get_date_slice, ('2022-05-09', '2022-05-10', '2022-05-11', '2022-05-12'))

    def test_filter_helpers(self):
        # Load test data from Dominaria Premier Draft.
        test_data = FramedData('DOM', 'PremierDraft', load_history=False)
        frame = test_data.card_frame(deck_color='', summary=True)

        # Check rarity filter
        filter_1 = rarity_filter('MR')
        filter_2 = rarity_filter(['M', 'R'])
        filter_3 = rarity_filter({'M', 'R'})
        num = 68
        self.assertRaises(TypeError, rarity_filter, None)
        self.assertEqual(filter_1(frame).sum(), num)
        self.assertEqual(filter_2(frame).sum(), num)
        self.assertEqual(filter_3(frame).sum(), num)

        # Check cmc filter
        filter_1 = cmc_filter(3)
        filter_2 = cmc_filter(3, op=">=")
        filter_3 = cmc_filter(3, op="<=")
        self.assertRaises(TypeError, cmc_filter, None)
        self.assertRaises(TypeError, cmc_filter, "None")
        self.assertRaises(TypeError, cmc_filter, 1, None)
        self.assertRaises(ValueError, cmc_filter, 1, "None")
        self.assertEqual(filter_1(frame).sum(), 46)
        self.assertEqual(filter_2(frame).sum(), 154)
        self.assertEqual(filter_3(frame).sum(), 141)

        # Check card color filter
        filter_1 = card_color_filter('WR')
        filter_2 = card_color_filter(['', 'W', 'R', 'WR'])
        filter_3 = card_color_filter({'', 'W', 'R', 'WR'})
        filter_4 = card_color_filter(subset('WR'))
        num = 110
        self.assertRaises(TypeError, card_color_filter, None)
        self.assertEqual(filter_1(frame).sum(), 2)
        self.assertEqual(filter_2(frame).sum(), num)
        self.assertEqual(filter_3(frame).sum(), num)
        self.assertEqual(filter_4(frame).sum(), num)

        # Check cast color filter
        filter_1 = cast_color_filter('WR')
        filter_2 = cast_color_filter(['', 'W', 'R', 'WR'])
        filter_3 = cast_color_filter({'', 'W', 'R', 'WR'})
        filter_4 = cast_color_filter(subset('WR'))
        num = 119
        self.assertRaises(TypeError, cast_color_filter, None)
        self.assertEqual(filter_1(frame).sum(), 1)
        self.assertEqual(filter_2(frame).sum(), num)
        self.assertEqual(filter_3(frame).sum(), num)
        self.assertEqual(filter_4(frame).sum(), num)

        # Compose functions
        filter_1 = compose_filters([cast_color_filter('W'), card_color_filter('W'), rarity_filter('R')])
        self.assertEqual(filter_1(frame).sum(), 6)


class TestDataLoader(unittest.TestCase):
    DATA_DIR_LOC = r'C:\Users\Zachary\Coding\GitHub'
    DATA_DIR_NAME = '17LandsData'

    def test_urls_no_date(self):
        loader = DataLoader('DOM', 'PremierDraft')

        str1 = loader._get_date_filter()
        date_str = r'&start_date=2020-01-01&end_date=' + str(date.today())
        self.assertEqual(str1, date_str)

        str1 = loader.get_card_rating_url()
        str2 = r'https://www.17lands.com/card_ratings/data?expansion=DOM&format=PremierDraft'
        self.assertEqual(str1, str2 + date_str)

        str1 = loader.get_card_rating_url('RW')
        str2 = r'https://www.17lands.com/card_ratings/data?expansion=DOM&format=PremierDraft&colors=RW'
        self.assertEqual(str1, str2 + date_str)

        str1 = loader.get_color_rating_url()
        str2 = r'https://www.17lands.com/color_ratings/data?expansion=DOM&event_type=PremierDraft&combine_splash=false'
        self.assertEqual(str1, str2 + date_str)

    def test_urls(self):
        loader = DataLoader('DOM', 'PremierDraft', date(2022, 4, 1))

        str1 = loader._get_date_filter()
        date_str = r'&start_date=2022-04-01&end_date=2022-04-01'
        self.assertEqual(str1, date_str)

        str1 = loader.get_card_rating_url()
        str2 = r'https://www.17lands.com/card_ratings/data?expansion=DOM&format=PremierDraft'
        self.assertEqual(str1, str2 + date_str)

        str1 = loader.get_card_rating_url('RW')
        str2 = r'https://www.17lands.com/card_ratings/data?expansion=DOM&format=PremierDraft&colors=RW'
        self.assertEqual(str1, str2 + date_str)

        str1 = loader.get_color_rating_url()
        str2 = r'https://www.17lands.com/color_ratings/data?expansion=DOM&event_type=PremierDraft&combine_splash=false'
        self.assertEqual(str1, str2 + date_str)

    def test_paths_no_date(self):
        loader = DataLoader('DOM', 'PremierDraft')

        str1 = loader.get_folder_path()
        dir_str = path.join(self.DATA_DIR_LOC, self.DATA_DIR_NAME, 'DOM', 'PremierDraft', 'ALL')
        self.assertEqual(str1, dir_str)

        str1 = loader.get_file_path('ColorRatings.json')
        str2 = path.join(dir_str, 'ColorRatings.json')
        self.assertEqual(str1, str2)

        self.assertFalse(loader.file_exists('SoupRecipe.json'))
        self.assertTrue(loader.file_exists('ColorRatings.json'))
        self.assertTrue(loader.file_exists('CardRatings.json'))

    def test_paths(self):
        loader = DataLoader('DOM', 'PremierDraft', date(2022, 4, 1))

        str1 = loader.get_folder_path()
        dir_str = path.join(self.DATA_DIR_LOC, self.DATA_DIR_NAME, 'DOM', 'PremierDraft', '2022-04-01')
        self.assertEqual(str1, dir_str)

        str1 = loader.get_file_path('ColorRatings.json')
        str2 = path.join(dir_str, 'ColorRatings.json')
        self.assertEqual(str1, str2)

        self.assertFalse(loader.file_exists('SoupRecipe.json'))
        self.assertTrue(loader.file_exists('ColorRatings.json'))
        self.assertTrue(loader.file_exists('CardRatings.json'))

    def test_file_validation(self):
        loader = DataLoader('DOM', 'PremierDraft', date(2022, 4, 1))
        self.assertEqual(loader.get_last_summary_update_time().date(), date(2022, 4, 24))

    def validate_returned_json(self, data, keys):
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        for key in keys:
            self.assertTrue(key in data[0])

    def test_get_card_data(self):
        loader = DataLoader('DOM', 'PremierDraft', date(2022, 4, 1))
        data = loader.get_card_data()
        self.validate_returned_json(data, CARD_KEYS)

    def test_get_meta_data(self):
        loader = DataLoader('DOM', 'PremierDraft', date(2022, 4, 1))
        data = loader.get_meta_data()
        self.validate_returned_json(data, META_KEYS)


class TestLoadedData(unittest.TestCase):
    def validate_returned_json(self, data, keys):
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        for key in keys:
            self.assertIn(key, data[0])

    def test_date_logic(self):
        loaded = LoadedData('DOM', 'PremierDraft')
        self.assertIsNotNone(FormatMetadata.get_metadata('DOM', 'PremierDraft'))

        # Valid pull
        refresh = loaded._is_historic_data_available(datetime(2022, 4, 2, 0, 0), datetime(2022, 4, 3, 2, 0))
        self.assertTrue(refresh)
        # Before release
        refresh = loaded._is_historic_data_available(datetime(2022, 3, 2, 0, 0), datetime(2022, 4, 3, 2, 0))
        self.assertFalse(refresh)
        # After finish
        refresh = loaded._is_historic_data_available(datetime(2022, 5, 2, 0, 0), datetime(2022, 4, 3, 2, 0))
        self.assertFalse(refresh)
        # No data exists yet
        refresh = loaded._is_historic_data_available(datetime(2022, 4, 4, 0, 0), datetime(2022, 4, 3, 2, 0))
        self.assertFalse(refresh)

        # Valid pull
        refresh = loaded._is_summary_data_stale(datetime(2022, 4, 2, 12, 0), datetime(2022, 4, 3, 2, 0))
        self.assertTrue(refresh)
        # After finish, but with possible updates
        refresh = loaded._is_summary_data_stale(datetime(2022, 4, 9, 12, 0), datetime(2022, 4, 10, 2, 0))
        self.assertTrue(refresh)
        # Data is not stale
        refresh = loaded._is_summary_data_stale(datetime(2022, 4, 2, 12, 0), datetime(2022, 4, 2, 2, 0))
        self.assertFalse(refresh)
        # After finish
        refresh = loaded._is_summary_data_stale(datetime(2022, 5, 2, 12, 0), datetime(2022, 4, 3, 2, 0))
        self.assertFalse(refresh)
        # No data exists yet
        refresh = loaded._is_summary_data_stale(datetime(2022, 4, 4, 12, 0), datetime(2022, 4, 3, 2, 0))
        self.assertFalse(refresh)

    def test_get_summary_data(self):
        loaded = LoadedData('DOM', 'PremierDraft')
        card, meta = loaded.get_summary_data()
        self.assertIsInstance(card, dict)
        self.validate_returned_json(card[''], CARD_KEYS)
        self.validate_returned_json(meta, META_KEYS)

    def test_get_historic_data(self):
        loaded = LoadedData('DOM', 'PremierDraft')
        card, meta = loaded.get_historic_data()
        date_tmp = '2022-04-0x'

        self.assertIsInstance(card, dict)
        self.assertIsInstance(card['2022-04-01'], dict)
        self.validate_returned_json(card['2022-04-01'][''], CARD_KEYS)

        self.assertIsInstance(meta, dict)
        self.validate_returned_json(meta['2022-04-01'], META_KEYS)

        for i in range(1, 9):
            date_str = date_tmp.replace('x', str(i))
            self.assertIn(date_str, card)
            self.assertIn(date_str, meta)


class TestDataFramer(unittest.TestCase):
    ARCHETYPE_COLS = ['Colors', 'Splash', 'Wins', 'Games', 'Win %']
    CARD_COLS = ['# Seen', 'ALSA', '# Picked', 'ATA', '# GP', 'GP WR', 'GP GW', '# OH', 'OH WR', 'OH GW',
                 '# GD', 'GD WR', 'GD GW', '# GIH', 'GIH WR', 'GIH GW', '# GND', 'GND WR', 'GND GW', 'IWD',
                 'Rarity', 'Color', 'Cast Color', 'CMC',
                 'Type Line', 'Supertypes', 'Types', 'Subtypes', 'Power', 'Toughness']

    def test_gen_hist(self):
        framer = DataFramer('DOM', 'PremierDraft')
        framer.gen_hist()
        self.assertIsInstance(framer.GROUPED_ARCHETYPE_HISTORY_FRAME, DataFrame)
        self.assertIsInstance(framer.SINGLE_ARCHETYPE_HISTORY_FRAME, DataFrame)
        self.assertIsInstance(framer.CARD_HISTORY_FRAME, DataFrame)

        self.assertListEqual(list(framer.GROUPED_ARCHETYPE_HISTORY_FRAME.columns), self.ARCHETYPE_COLS)
        self.assertListEqual(list(framer.SINGLE_ARCHETYPE_HISTORY_FRAME.columns), self.ARCHETYPE_COLS)
        self.assertListEqual(list(framer.CARD_HISTORY_FRAME.columns), self.CARD_COLS)

    def test_gen_summary(self):
        framer = DataFramer('DOM', 'PremierDraft')
        framer.gen_summary()
        self.assertIsInstance(framer.GROUPED_ARCHETYPE_SUMMARY_FRAME, DataFrame)
        self.assertIsInstance(framer.SINGLE_ARCHETYPE_SUMMARY_FRAME, DataFrame)
        self.assertIsInstance(framer.CARD_SUMMARY_FRAME, DataFrame)

        self.assertListEqual(list(framer.GROUPED_ARCHETYPE_SUMMARY_FRAME.columns), self.ARCHETYPE_COLS)
        self.assertListEqual(list(framer.SINGLE_ARCHETYPE_SUMMARY_FRAME.columns), self.ARCHETYPE_COLS)
        self.assertListEqual(list(framer.CARD_SUMMARY_FRAME.columns), self.CARD_COLS)


class TestFramedData(unittest.TestCase):
    # TODO: Complete this test.
    def test_(self):
        framer = FramedData('DOM', 'PremierDraft')

        framer.deck_group_frame()
        framer.deck_group_frame(summary=True)
        framer.deck_archetype_frame()
        framer.deck_archetype_frame(summary=True)
        framer.card_frame()
        framer.card_frame(summary=True)

        # frame = card_frame(date=('2022-04-01', '2022-04-08'))
        # framer.aggregate_card_frame()

        self.assertTrue(False)
