import os
import time
import re
from datetime import datetime, date
from bs4 import BeautifulSoup
from selenium import webdriver

from core.utilities import save_json_file
from core.game_metadata.utils.consts import DATE_FMT
from core.game_metadata.utils.settings import EVENT_CALENDAR_JSON

parse_str = r"([A-Z][a-z][a-z] [\d][\d], [\d][\d][\d][\d]) . ([A-Z][a-z][a-z] [\d][\d], [\d][\d][\d][\d])"
finder = re.compile(parse_str)

# TODO: These change over time. Try and parse them somehow.
PANEL_CLASS_NAME = "sc-bXmInU fTTNsa"
TEXT_CLASS_NAME = "sc-ezHdRe dZLpki"

expansion_name_mapping = {
    "Murders at Karlov Manor": "MKM",
    "Lost Caverns of Ixalan": "LCI",
    "Wilds of Eldraine": "WOE",
    "Lord of the Rings: Tales of Middle-earth": "LTR",
    "March of the Machine": "MOM",
    "Shadows Remastered": "SIR",
    "Phyrexia: All Will Be One": "ONE",
    "All Will Be One": "ONE",
    "The Brothers' War": "BRO",
    "Dominaria United": "DMU",
    "New Capenna": "SNC",
    "Neon Dynasty": "NEO",
    "Crimson Vow": "VOW",
    "VOW": "VOW",
    "Midnight Hunt": "MID",
    "Dominaria": "DOM",
    "War of the Spark": "WAR",
    "Forgotten Realms": "AFR",
    "Zendikar Rising": "ZNR",
    "Core Set 2020": "M20",
    "Ikoria: Lair of Behemoths": "IKO",
    "Core Set 2021": "M21",
    "Strixhaven": "STX",
    "Theros Beyond Death": "THB",
    "Kaladesh Remastered": "KLR",
    "Throne of Eldraine": "ELD",
    "Kaldheim": "KHM",
    "Baldur's Gate": "HBG",
    "Ravnica Allegiance": "RNA",
    "Ravnica": "GRN",
    "Amonkhet Remastered": "AKR",
}

event_type_mapping = {
    'Premier Draft': 'PremierDraft',
    'Traditional Draft': 'TradDraft',
    'Quick Draft': 'QuickDraft',
    'Traditional Sealed': 'Sealed',
    'Sealed': 'TradSealed'
}

event_type_ordering = {
    'PremierDraft': 0,
    'TradDraft': 1,
    'QuickDraft': 2,
    'Sealed': 3,
    'TradSealed': 4,
}


def get_true_html(url: str) -> str:
    """
    Gets the 'real' html content of a website, by loading it through an instance of Firefox.
    :param url:
    :return:
    """
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.close()
    driver.quit()
    os.remove(r'geckodriver.log')
    return html


def parse_event_calendar_webpage() -> list[tuple[str, date, date]]:
    """
    Parses the content of 'https://mtgarena.pro/mtga-event-calendar/' into a list
    of event names and dates.
    :return: A list of events: name, start date, end date.
    """
    def parse_item(item) -> tuple[str, date, date]:
        event = item.find('div', {"class": TEXT_CLASS_NAME})
        event_name = event.text.replace('_', ' ')
        start, end = finder.findall(item.text)[0]
        fmt = "%b %d, %Y"
        start_date = datetime.strptime(start, fmt).date()
        end_date = datetime.strptime(end, fmt).date()
        return event_name, start_date, end_date

    url = 'https://mtgarena.pro/mtga-event-calendar/'
    html = get_true_html(url)
    soup = BeautifulSoup(html, features="html.parser")
    content_table = soup.find_all('div', {"class": PANEL_CLASS_NAME})
    return [parse_item(item) for item in content_table]


def generate_limited_information(event_list: list[tuple[str, date, date]]) -> list[tuple[str, str, date, date]]:
    """
    Generates limited event information based on event data.
    :param event_list: The event information: name, start, end
    :return: The limited event information: set_code, event_type, start, end
    """
    def parse_event_tuple() -> tuple[str, str, date, date] | None:
        expansion = event[0].replace(format_type, '').strip()
        if expansion.startswith(':'):
            expansion = expansion[2:]

        # Map expansion to set code.
        is_alchemy = False
        if expansion.endswith('Alchemy'):
            is_alchemy = True
            expansion = expansion.replace('Alchemy', '').strip()

        if expansion in expansion_name_mapping:
            expansion_code = expansion_name_mapping[expansion]
            if is_alchemy:
                expansion_code = f"Y{expansion_code}"
        else:
            return None

        return expansion_code, event_type_mapping[format_type], event[1], event[2]

    ret = list()
    for event in event_list:
        for format_type in event_type_mapping.keys():
            if format_type in event[0]:
                val = parse_event_tuple()
                if val:
                    ret.append(val)
                break

    return ret


def gen_event_calendar_dict(event_list: list[tuple[str, str, date, date]]) ->\
        dict[str, dict[str, list[tuple[str, str]]]]:
    ordered_events = list(event_list)
    ordered_events.sort(key=lambda x: (x[0], event_type_ordering[x[1]], x[2]))

    ret = dict()
    for e in ordered_events:
        if not e[0] in ret:
            ret[e[0]] = dict()

        if not e[1] in ret[e[0]]:
            ret[e[0]][e[1]] = list()

        ret[e[0]][e[1]].append((e[2].strftime(DATE_FMT), e[3].strftime(DATE_FMT)))
    return ret


def main():
    events = parse_event_calendar_webpage()
    limited_events = generate_limited_information(events)
    event_time_dict = gen_event_calendar_dict(limited_events)
    save_json_file(r'..\core\game_metadata\utils', EVENT_CALENDAR_JSON, event_time_dict)


if __name__ == "__main__":
    main()
