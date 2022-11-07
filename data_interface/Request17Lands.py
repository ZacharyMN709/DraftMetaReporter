from typing import Optional, Union, NoReturn
from datetime import date, datetime
import json
import pandas as pd

from data_interface.Requester import Requester_2
import utilities.utils.settings as settings


# Adapted from 'https://github.com/diogojapinto/mtg-data-mining/blob/main/utils/api_clients/seventeen_lands/client.py'
class Request17Lands(Requester_2):
    BASE_URL = 'https://www.17lands.com'
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
    DETAILS_URL = 'https://www.17lands.com/data/details'

    def __init__(self, tries: Optional[int] = None, fail_delay: Optional[float] = None,
                 success_delay: Optional[float] = None):
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

    def get_color_ratings(self, expansion: str,
                          event_type: Optional[str] = None,
                          start_date: Optional[date] = None,
                          end_date: Optional[date] = None,
                          combine_splash: bool = False,
                          user_group: Optional[str] = None) -> pd.DataFrame:

        start_date = start_date or settings.DEFAULT_DATE
        end_date = end_date or date.today()

        params = {
            'expansion': expansion,
            'event_type': event_type or settings.DEFAULT_FORMAT,
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

    def get_card_ratings(self, expansion: str,
                         event_type: Optional[str] = None,
                         start_date: Optional[date] = None,
                         end_date: Optional[date] = None,
                         user_group: Optional[str] = None,
                         deck_colors: Optional[str] = None) -> pd.DataFrame:

        start_date = start_date or settings.DEFAULT_DATE
        end_date = end_date or date.today()

        params = {
            'expansion': expansion,
            'format': event_type or settings.DEFAULT_FORMAT,
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

    def get_card_evaluations(self, expansion: str,
                             event_type: Optional[str] = None,
                             start_date: Optional[date] = None,
                             end_date: Optional[date] = None,
                             rarity: Optional[str] = None,
                             color: Optional[str] = None) -> pd.DataFrame:

        start_date = start_date or settings.DEFAULT_DATE
        end_date = end_date or date.today()

        params = {
            'expansion': expansion,
            'format': event_type or settings.DEFAULT_FORMAT,
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

    def get_trophy_deck_metadata(self, expansion: str, event_type: Optional[str] = None) -> pd.DataFrame:
        params = {
            'expansion': expansion,
            'format': event_type or settings.DEFAULT_FORMAT
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

        return result

    def get_deck(self, draft_id: str, deck_index: int = 0) -> dict:
        params = {
            'draft_id': draft_id,
            'deck_index': deck_index
        }
        return self.request(url=self.DECK_URL, params=params).json()

    def get_details(self, draft_id: str) -> None:
        params = {
            'draft_id': draft_id,
        }

        result = self.request(url=self.DETAILS_URL, params=params).json()
        return result

    def get_draft(self, draft_id: str) -> Union[dict, NoReturn]:
        params = {
            'draft_id': draft_id
        }

        # Process built-in JSON
        text = self.request(url=self.DRAFT_LOG_URL, params=params).text[6:-2]
        result = json.loads(text)

        # Only return results if payload is complete
        if result['type'] != 'complete':  # pragma: nocover
            raise ValueError(f"Response is not complete. Response type: '{result['type']}'")

        return result['payload']
