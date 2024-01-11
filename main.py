import json

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import re

import pprint

urllib3.disable_warnings(InsecureRequestWarning)
GAMER_USERNAME = "ChiefChirpa"
LOGIN_MESSAGE = "зашёл на сервер"
LOGOUT_MESSAGE = "вышел с сервера"

HITECH_LOGS_LINK = "https://logs1.sidemc.net/m1logs/Hitech_logger_public_logs/Logs/"
DATE_FORMAT = "%d-%m-%Y"
LOG_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"


def get_needed_dates():
  dates = input("Insert 2 dates separated by space(e.g. 01-01-2024 03-01-2024): ")
  dates_lst = dates.split()
  date_object_from = datetime.strptime(dates_lst[0], DATE_FORMAT).date()
  date_object_till = datetime.strptime(dates_lst[1], DATE_FORMAT).date()
  if date_object_till < date_object_from:
    print("Second date can't be less then first!")
    quit()

  date_difference = date_object_till - date_object_from

  all_dates = [(date_object_from + timedelta(days=i)).strftime(DATE_FORMAT) for i in range(date_difference.days + 1)]
  return all_dates


def get_text_files_links(dates: list) -> list:
  response = requests.get(url=HITECH_LOGS_LINK, verify=False)
  html_content = response.text
  soup = BeautifulSoup(html_content, "html.parser")

  href_texts = [a.text for a in soup.find_all("a", href=True) if a.text != "../"]
  return [(file_name, HITECH_LOGS_LINK + file_name) for file_name in href_texts if file_name.split(".")[0] in dates]


def gamers_login_logout_messages(link):
  """
  Function to get strings of user login and logout message(e.g. [<time>] <user> left the game)
  """
  response = requests.get(link[1], verify=False)
  login_logout_messages = []
  if response.status_code == 200:
    login_logout_messages = [line for line in response.text.split('\n') if GAMER_USERNAME in line and (LOGIN_MESSAGE in line or LOGOUT_MESSAGE in line)]

  return {link[0]: login_logout_messages}


def extract_login_logout_dates(log_lines: dict):
  """
  Function to extract date from strings of user login and logout messages and process them
  """
  user_data = {}
  i = 0
  for log_line in list(log_lines.values())[0]:
    date_time_pattern = re.compile(r'\[(.*?)\]')
    date_time_match = date_time_pattern.search(log_line)
    date_time_str = date_time_match.group(1) if date_time_match else None

    if date_time_str:
        log_datetime = datetime.strptime(date_time_str, LOG_DATE_FORMAT)
        if "зашёл на сервер" in log_line:
          user_data.update({i: {"login": date_time_str}})
        elif "вышел с сервера" in log_line:
          user_data.update({i: {"logout": date_time_str}})
    else:
        print("Datetime not found in the log line.")
    i += 1
  return user_data

def create_user_file(user_data: dict):
  todays_date = date.today().strftime(DATE_FORMAT)

  with open(f"{GAMER_USERNAME}-{todays_date}", "w") as file:
    json.dump(user_data, file, indent=4)
  pprint.pprint(user_data)


def main():
  needed_dates = get_needed_dates()
  user_data = {}
  for link in get_text_files_links(needed_dates):
    user_data.update({f"{GAMER_USERNAME} - {link[0]}": extract_login_logout_dates(gamers_login_logout_messages(link))})
  create_user_file(user_data=user_data)


if __name__ == "__main__":
  main()
