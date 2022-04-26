import unittest
from datetime import date
from os import path

from data_fetching.utils.pandafy import gen_card_frame, gen_meta_frame

from data_fetching import DataLoader, LoadedData, DataFramer, FramedData, SetManager, CentralManager


class TestUtils(unittest.TestCase):
    def test_gen_card_frame(self):
        card_data = [
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

        card_frame = gen_card_frame(card_data)
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
        meta_data = [
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
            {'is_summary': False, 'color_name': 'Boros (RW)', 'wins': 85, 'games': 142}]

        sum_frame, arc_frame = gen_meta_frame(meta_data)
        self.assertEqual(len(sum_frame), 2)
        self.assertEqual(len(arc_frame), 10)

        def compare_summary_frame(row_name: str, games: int, wins: int, winrate: float, splash: bool):
            self.assertEqual(sum_frame.loc[row_name]['Games'], games)
            self.assertEqual(sum_frame.loc[row_name]['Wins'], wins)
            self.assertAlmostEqual(sum_frame.loc[row_name]['Win %'], winrate, delta=0.05)
            self.assertEqual(sum_frame.loc[row_name]['Splash'], splash)

        def compare_archetype_frame(row_name: str, games: int, wins: int, winrate: float, splash: bool):
            self.assertEqual(arc_frame.loc[row_name]['Games'], games)
            self.assertEqual(arc_frame.loc[row_name]['Wins'], wins)
            self.assertAlmostEqual(arc_frame.loc[row_name]['Win %'], winrate, delta=0.05)
            self.assertEqual(arc_frame.loc[row_name]['Splash'], splash)

        compare_summary_frame('Two-color', 1967, 1142, 58.060, False)
        compare_summary_frame('Two-color + Splash', 697, 395, 56.670060, True)

        compare_archetype_frame('UR', 608, 361, 59.380, False)

    def test_gen_meta_frame_empty(self):
        sum_frame, arc_frame = gen_meta_frame(list())
        self.assertEqual(len(sum_frame), 0)
        self.assertEqual(len(arc_frame), 0)


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
        self.assertEqual(loader.get_last_write_time().date(), date(2022, 4, 24))

    def test_get_card_data(self):
        loader = DataLoader('DOM', 'PremierDraft', date(2022, 4, 1))
        loader.get_card_data()

    def test_get_meta_data(self):
        loader = DataLoader('DOM', 'PremierDraft', date(2022, 4, 1))
        loader.get_meta_data()

    def test_get_day_data(self):
        loader = DataLoader('DOM', 'PremierDraft', date(2022, 4, 1))
        loader.get_day_data()


class TestLoadedData(unittest.TestCase):
    def test_get_day_data(self):
        loaded = LoadedData('DOM', 'PremierDraft')
        loaded.get_day_data(date(2022, 4, 1))

    def test_get_summary_data(self):
        loaded = LoadedData('DOM', 'PremierDraft')
        loaded.get_summary_data()

    def test_get_historic_data(self):
        loaded = LoadedData('DOM', 'PremierDraft')
        loaded.get_historic_data()


class TestDataFramer(unittest.TestCase):
    def test_data_framer(self):
        framer = DataFramer('DOM', 'PremierDraft')
        self.assertEqual(framer.SET, 'DOM')
        self.assertEqual(framer.FORMAT, 'PremierDraft')
        pass


class TestFramedData(unittest.TestCase):
    def test_(self):
        pass


class TestSetManager(unittest.TestCase):
    def test_set_manager(self):
        manager = SetManager('NEO')
        # manager.reload_data()