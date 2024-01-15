import json
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import re


urllib3.disable_warnings(InsecureRequestWarning)
LOGIN_MESSAGE = "зашёл на сервер"
LOGOUT_MESSAGE = "вышел с сервера"

HITECH_LOGS_LINK = "https://logs1.sidemc.net/m1logs/Hitech_logger_public_logs/Logs/"
DATE_FORMAT = "%d-%m-%Y"
LOG_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"

def get_needed_dates(start_date: str, end_date: str):
    date_object_from = datetime.strptime(start_date, DATE_FORMAT).date()
    date_object_till = datetime.strptime(end_date, DATE_FORMAT).date()
    if date_object_till < date_object_from:
        print("Second date can't be less than the first!")

    date_difference = date_object_till - date_object_from

    all_dates = [(date_object_from + timedelta(days=i)).strftime(DATE_FORMAT) for i in range(date_difference.days + 1)]
    return all_dates

def get_text_files_links(dates: list) -> list:
    response = requests.get(url=HITECH_LOGS_LINK, verify=False)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    href_texts = [a.text for a in soup.find_all("a", href=True) if a.text != "../"]
    return [(file_name, HITECH_LOGS_LINK + file_name) for file_name in href_texts if file_name.split(".")[0] in dates]

# def gamers_login_logout_messages(link):
#     response = requests.get(link[1], verify=False)
#     login_logout_messages = []
#     if response.status_code == 200:
#         login_logout_messages = [line for line in response.text.split('\n') if any(username in line for username in USERNAME_LIST)
#                                   and (LOGIN_MESSAGE in line or LOGOUT_MESSAGE in line)]
#
#     return {link[0]: login_logout_messages}
#
# def extract_login_logout_dates(log_lines: dict):
#     user_data = {}
#     i = 0
#     for log_line in list(log_lines.values())[0]:
#         date_time_pattern = re.compile(r'\[(.*?)\]')
#         date_time_match = date_time_pattern.search(log_line)
#         date_time_str = date_time_match.group(1) if date_time_match else None
#
#         if date_time_str:
#             log_datetime = datetime.strptime(date_time_str, LOG_DATE_FORMAT)
#             username = [username for username in USERNAME_LIST if username in log_line][0]
#             if username not in user_data:
#                 user_data[username] = {"login": [], "logout": []}
#
#             if "зашёл на сервер" in log_line:
#                 user_data[username]["login"].append(date_time_str)
#             elif "вышел с сервера" in log_line:
#                 user_data[username]["logout"].append(date_time_str)
#         else:
#             print("Datetime not found in the log line.")
#         i += 1
#     return user_data
#
# def create_user_file(user_data: dict):
#     todays_date = date.today().strftime(DATE_FORMAT)
#
#     for username, data in user_data.items():
#         with open(f"{username}-{todays_date}.json", "w") as file:
#             json.dump(data, file, indent=4)
#         pprint.pprint(data)

def main(*user_data):
    usernames = user_data[0]
    start_date = user_data[1]
    end_date = user_data[2]
    print(get_text_files_links(get_needed_dates(start_date, end_date)))
