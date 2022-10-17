from typing import Optional
from datetime import date, datetime
import json
import pandas as pd

from Utilities.SiteRequests.Requester import Requester, Requester_2
from Utilities.utils import TRIES, FAIL_DELAY, SUCCESS_DELAY
from Utilities.utils.settings import DEFAULT_FORMAT, DEFAULT_DATE


# Adapted from 'https://github.com/diogojapinto/mtg-data-mining/blob/main/utils/api_clients/seventeen_lands/client.py'
class Request17Lands(Requester_2):
    COLOR_URL = 'https://www.17lands.com/data/colors'
    EXPANSIONS_URL = 'https://www.17lands.com/data/expansions'
    FORMATS_URL = 'https://www.17lands.com/data/formats'
    PLAY_DRAW_URL = 'https://www.17lands.com/data/play_draw'
    COLOR_RATING_URL = 'https://www.17lands.com/color_ratings/data'
    CARD_RATING_URL = 'https://www.17lands.com/card_ratings/data'
    CARD_EVAL_URL = 'https://www.17lands.com/card_evaluation_metagame/data'
    TROPHY_URL = 'https://www.17lands.com/data/trophies'
    DRAFT_LOG_URL = 'https://www.17lands.com/data/draft/stream'
    DECK_URL = 'https://www.17lands.com/data/deck'

    def __init__(self, tries: int = TRIES, fail_delay: int = FAIL_DELAY, success_delay: int = SUCCESS_DELAY) -> None:
        super().__init__(tries, fail_delay, success_delay)

    def get_colors(self) -> list[str]:
        return self.request(url=self.COLOR_URL).json()

    def get_expansions(self) -> list[str]:
        return self.request(url=self.EXPANSIONS_URL).json()

    def get_event_types(self) -> list[str]:
        return self.request(url=self.FORMATS_URL).json()

    def get_play_draw_stats(self) -> pd.DataFrame:
        result = self.request(url=self.PLAY_DRAW_URL).json()
        play_draw_stats = pd.DataFrame(result)
        return play_draw_stats

    def get_color_ratings(self, expansion: str, event_type: str = DEFAULT_FORMAT,
                          start_date: Optional[date] = DEFAULT_DATE, end_date: Optional[date] = date.today(),
                          combine_splash: bool = False, user_group: Optional[str] = None) -> pd.DataFrame:
        params = {
            'expansion': expansion,
            'event_type': event_type,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'combine_splash': combine_splash,
            'user_group': user_group
        }

        result = self.request(url=self.COLOR_RATING_URL, params=params).json()

        # Apply a more intuitive columns ordering
        unsorted_df = pd.DataFrame(result)
        columns_order = [
            'is_summary',
            'color_name',
            'wins',
            'games'
        ]

        color_ratings = unsorted_df.loc[:, columns_order]

        return color_ratings

    def get_card_ratings(self, expansion: str, event_type: str = DEFAULT_FORMAT,
                         start_date: Optional[date] = DEFAULT_DATE, end_date: Optional[date] = date.today(),
                         user_group: Optional[str] = None, deck_colors: Optional[str] = None) -> pd.DataFrame:
        params = {
            'expansion': expansion,
            'format': event_type,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'user_group': user_group,
            'colors': deck_colors
        }

        result = self.request(url=self.CARD_RATING_URL, params=params).json()

        # Apply a more intuitive columns ordering, and remove URLs and sideboard metrics
        unsorted_df = pd.DataFrame(result)
        sorted_cols = [
            'name',
            'color',
            'rarity',
            'seen_count',
            'avg_seen',
            'pick_count',
            'avg_pick',
            'game_count',
            'win_rate',
            'opening_hand_game_count',
            'opening_hand_win_rate',
            'drawn_game_count',
            'drawn_win_rate',
            'ever_drawn_game_count',
            'ever_drawn_win_rate',
            'never_drawn_game_count',
            'never_drawn_win_rate',
            'drawn_improvement_win_rate'
        ]
        sorted_df = unsorted_df.loc[:, sorted_cols]

        # Rename the metrics for more standard ones
        card_ratings = sorted_df.rename(columns={
            'avg_seen': 'avg_last_seen_at',
            'avg_pick': 'avg_taken_at',
            'game_count': 'games_played_count',
            'win_rate': 'games_played_win_rate',
            'ever_drawn_game_count': 'in_hand_game_count',
            'ever_drawn_win_rate': 'in_hand_win_rate',
            'never_drawn_game_count': 'not_drawn_game_count',
            'never_drawn_win_rate': 'not_drawn_win_rate',
            'drawn_improvement_win_rate': 'improvement_when_drawn'
        })

        return card_ratings

    def get_card_evaluations(self, expansion: str, event_type: str = DEFAULT_FORMAT,
                             start_date: Optional[date] = DEFAULT_DATE, end_date: Optional[date] = date.today(),
                             rarity: Optional[str] = None, color: Optional[str] = None) -> pd.DataFrame:
        params = {
            'expansion': expansion,
            'format': event_type,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'rarity': rarity,
            'color': color
        }

        result = self.request(url=self.CARD_EVAL_URL, params=params).json()

        # Tidy up data into a dataframe of one row per date-card combination
        digested_result_accum = []
        for d_i, day in enumerate(result['dates']):
            for c_i, card in enumerate(result['cards']):
                digested_result_accum.append({
                    'date': datetime.strptime(day, '%Y-%m-%d'),
                    'name': card,
                    'pick_n': result['data'][d_i][c_i]['pick_n'],
                    'pick_avg': result['data'][d_i][c_i]['pick_avg'],
                    'seen_n': result['data'][d_i][c_i]['seen_n'],
                    'seen_avg': result['data'][d_i][c_i]['seen_avg']
                })
        digested_result_df = pd.DataFrame(digested_result_accum).drop_duplicates(ignore_index=True)

        # Rename the metrics for more standard ones
        card_evaluations = digested_result_df.rename(columns={
            'pick_n': 'pick_count',
            'pick_avg': 'avg_taken_at',
            'seen_n': 'seen_count',
            'seen_avg': 'avg_last_seen_at'
        })

        return card_evaluations

    def get_trophy_decks(self, expansion: str, event_type: str = DEFAULT_FORMAT) -> pd.DataFrame:
        params = {
            'expansion': expansion,
            'format': event_type
        }

        result = self.request(url=self.TROPHY_URL, params=params).json()

        # Apply a more intuitive columns ordering
        unsorted_df = pd.DataFrame(result)
        sorted_cols = [
            'time',
            'colors',
            'wins',
            'losses',
            'start_rank',
            'end_rank',
            'aggregate_id',
            'deck_index',
        ]
        sorted_df = unsorted_df.loc[:, sorted_cols]

        # Keep column names uniform and intuitive
        trophy_decks = sorted_df.rename(columns={'aggregate_id': 'draft_id'})

        # Change time column data type
        trophy_decks.loc[:, 'time'] = pd.to_datetime(trophy_decks.time)

        return trophy_decks

    def get_draft(self, draft_id: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        params = {
            'draft_id': draft_id
        }

        result = self.request(url=self.DRAFT_LOG_URL, params=params)

        # Process built-in JSON
        response_obj = json.loads(result.text[6:-2])

        # Only return results if payload is complete
        if response_obj['type'] != 'complete':
            raise ValueError(f"Response is not complete. Response type: '{response_obj['type']}'")

        # Parse payload
        payload = response_obj['payload']
        expansion = payload['expansion']

        # Parse picks
        picks_accum = []
        for pick in payload['picks']:
            picks_accum.append({
                'expansion': expansion,
                'pack_number': pick['pack_number'],
                'pick_number': pick['pick_number'],
                'colors': pick['colors'],
                'pick': pick['pick']['name'],
                'available': [a['name'] for a in pick['available']],
                'known_missing': [m['name'] for m in pick['known_missing']],
                'pool': [p['name'] for p in pick['pool']],
                'possible_maindeck': [
                    m['name']
                    for m in [
                        i for l in pick['possible_maindeck']
                        for i in l
                    ]
                ],
                'probable_sideboard': [
                    s['name']
                    for s in [
                        i for l in pick['probable_sideboard']
                        for i in l
                    ]
                ]
            })
        picks = pd.DataFrame(picks_accum)

        # Parse and transform card performance data
        cards_performance = pd.DataFrame(payload['card_performance_data']) \
            .transpose() \
            .reset_index() \
            .rename(columns={
                'index': 'name',
                'total_times_seen': 'seen_count',
                'avg_seen_position': 'avg_last_seen_at',
                'total_times_picked': 'pick_count',
                'avg_pick_position': 'avg_taken_at'
            })

        return picks, cards_performance

    def get_deck(self, draft_id: str, deck_index: int) -> tuple[pd.DataFrame, dict[str, str]]:
        params = {
            'draft_id': draft_id,
            'deck_index': deck_index
        }

        result = self.request(url=self.DECK_URL, params=params).json()

        # Compile a deck dataframe
        deck_accum = []
        for group in result['groups']:
            for card in group['cards']:
                deck_accum.append({
                    'group': group['name'],
                    'name': card['name']
                })
        deck = pd.DataFrame(deck_accum)

        # Compile deck metadata
        event_info = result['event_info']
        deck_metadata = {
            'expansion': event_info['expansion'],
            'event_type': event_info['format'],
            'wins': event_info['wins'],
            'losses': event_info['losses'],
            'pool_link': event_info['pool_link'],
            'deck_links': event_info['deck_links'],
            'details_link': event_info['details_link'],
            'draft_link': event_info['draft_link'],
            'sealed_deck_tech_link': result['builder_link']
        }

        return deck, deck_metadata


if __name__ == "__main__":
    from Utilities.auto_logging import auto_log, LogLvl
    auto_log(LogLvl.DEBUG)
    DATA_DIR_LOC: str = r'C:\Users\Zachary\Coding\GitHub'
    caller = Request17Lands()

    colors = caller.get_colors()
    print(colors)

    expansions = caller.get_expansions()
    print(expansions)

    events = caller.get_event_types()
    print(events)

    play_draw = caller.get_play_draw_stats()
    print(play_draw)

    meta = caller.get_color_ratings("DMU")
    print(meta)
