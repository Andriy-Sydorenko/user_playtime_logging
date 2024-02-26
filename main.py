from datetime import datetime, timedelta

import requests
import urllib3
from bs4 import BeautifulSoup
from CTkMessagebox import CTkMessagebox
from urllib3.exceptions import InsecureRequestWarning

from utils import extract_datetime_from_log_string

urllib3.disable_warnings(InsecureRequestWarning)

LOGIN_MESSAGES = ["зашёл", "зашёл на сервер", ]
LOGOUT_MESSAGES = ["вышел", "вышел с сервера", ]

SERVERS = {
    "HiTech": "https://logs1.sidemc.net/m1logs/Hitech_logger_public_logs/Logs/",
    "MagicNew": "https://logs1.sidemc.net/m1logs/Magicnew_public_logs/",
    "TechnoMagic": "https://logs1.sidemc.net/m1logs/Technomagic_logger_public_logs/Logs/",
    "TechnoMagicRPG": "https://logs1.sidemc.net/m1logs/TMRPG_public_logs/",
    "MagicNew Test Server": "https://logs1.sidemc.net/m1logs/Magicnew_ServerTest_public_logs/",
}

DATE_FORMAT = "%d-%m-%Y"
LOG_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"


def get_needed_dates(start_date: str, end_date: str):
    date_object_from = datetime.strptime(start_date, DATE_FORMAT).date()
    date_object_till = datetime.strptime(end_date, DATE_FORMAT).date()

    date_difference = date_object_till - date_object_from

    all_dates = [(date_object_from + timedelta(days=i)).strftime(DATE_FORMAT) for i in range(date_difference.days + 1)]
    return all_dates


def get_text_files_links(dates: list, server_url: str) -> list[tuple]:
    try:
        response = requests.get(url=server_url, verify=False)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        href_texts = [a.text for a in soup.find_all("a", href=True) if a.text != "../"]
        return [(file_name, server_url + file_name) for file_name in href_texts if file_name.split(".")[0] in dates]
    except requests.exceptions.ConnectionError:
        CTkMessagebox(title="Problems with connection!",
                      message="Check your internet connection!",
                      icon="warning",
                      option_1="Ok")


def gamers_login_logout_messages(links: list[tuple], usernames: list[str]):
    users_data = {}
    for link in links:
        response = requests.get(link[1], verify=False)
        if response.status_code == 200:
            for username in usernames:
                if username not in users_data:
                    users_data[username] = []

                user_messages = [
                    line for line in response.text.split("\n") if
                    any(f"{username.strip()} {login_message}" in line
                        for login_message in LOGIN_MESSAGES)
                    or any(f"{username.strip()} {logout_message}" in line
                           for logout_message in LOGOUT_MESSAGES)
                ]

                users_data[username].extend(user_messages)
        else:
            CTkMessagebox(title="Connection problem!",
                          message="Maybe logs URL was changed!",
                          icon="cancel",
                          option_1="Ok")

    return users_data


def gamers_events_wins(links: list[tuple]) -> dict:
    user_wins = {}
    for link in links:
        response = requests.get(link[1], verify=False)
        if response.status_code == 200:
            lines = response.text.split("\n")
            for line in lines:
                if "/ereward" in line:
                    try:
                        player_username = line.split("/ereward")[1].strip()
                        if player_username in user_wins:
                            user_wins[player_username] += 1
                        else:
                            user_wins[player_username] = 1

                    except IndexError:
                        continue

        else:
            CTkMessagebox(title="Connection problem!",
                          message="Maybe logs URL was changed!",
                          icon="cancel",
                          option_1="Ok")
    return user_wins


def format_event_winners_data(event_winners_data: dict) -> str:
    formatted_counts = [f"{username}={wins_count}" for username, wins_count in event_winners_data.items()]
    return ", ".join(formatted_counts)


def count_playtime(days_count: int, users_data: dict):
    users_playtime = {}
    for user in users_data.keys():
        total_playtime = timedelta()
        user_data: list = users_data[user]
        if not user_data:
            continue
        if "вышел с сервера" in user_data[0] or "вышел" in user_data[0]:
            datetime_obj = extract_datetime_from_log_string(user_data.pop(0), LOG_DATE_FORMAT)
            midnight_day = datetime(datetime_obj.year, datetime_obj.month, datetime_obj.day)
            total_playtime += datetime_obj - midnight_day
        if "зашёл" in user_data[-1] or "зашёл на сервер" in user_data[-1]:
            datetime_obj = extract_datetime_from_log_string(user_data.pop(-1), LOG_DATE_FORMAT)
            midnight_day = datetime(datetime_obj.year,
                                    datetime_obj.month,
                                    datetime_obj.day,
                                    hour=23, minute=59, second=59)
            total_playtime += midnight_day - datetime_obj

        for login, logout in zip(user_data[0::2], user_data[1::2]):
            login_time = extract_datetime_from_log_string(login, LOG_DATE_FORMAT)
            logout_time = extract_datetime_from_log_string(logout, LOG_DATE_FORMAT)

            time_difference = logout_time - login_time
            total_playtime += time_difference

        average_playtime = total_playtime / days_count
        formatted_delta = "{:02}:{:02}:{:02}".format(
            average_playtime.seconds // 3600, (average_playtime.seconds // 60) % 60, average_playtime.seconds % 60
        )

        days = total_playtime.days
        hours, remainder = divmod(total_playtime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        total_hours = days * 24 + hours

        users_playtime.update({
            user: {
                "Total playtime": f"{total_hours}:{minutes}:{seconds}",
                "Average playtime": formatted_delta,
            }
        })
    return users_playtime


def get_users_playtime(usernames_list, start_date, end_date, server_name):
    usernames = list(set(usernames_list))
    start_date = start_date
    end_date = end_date
    server_url = SERVERS.get(server_name)
    links = get_text_files_links(get_needed_dates(start_date, end_date), server_url)
    try:
        days_count = len(links)
    except TypeError:
        return

    users_data = gamers_login_logout_messages(links, usernames)
    final_result = count_playtime(days_count, users_data)
    return final_result


def get_user_event_wins(start_date, end_date, server_name) -> str:
    server_url = SERVERS.get(server_name)
    links = get_text_files_links(get_needed_dates(start_date, end_date), server_url)
    event_winners_data = gamers_events_wins(links=links)
    formatted_event_winners_data = format_event_winners_data(event_winners_data)

    return formatted_event_winners_data
