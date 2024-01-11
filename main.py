import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

import pprint

urllib3.disable_warnings(InsecureRequestWarning)
GAMER_USERNAME = "ChiefChirpa"
LOGIN_MESSAGE = "зашёл на сервер"
LOGOUT_MESSAGE = "вышел с сервера"

HITECH_LOGS_LINK = "https://logs1.sidemc.net/m1logs/Hitech_logger_public_logs/Logs/"
DATE_FORMAT = "%d-%m-%Y"


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
  # Define a regular expression pattern to match the datetime format
  for log_line in list(log_lines.values())[0]:
    date_time_pattern = re.compile(r'\[(.*?)\]')
    date_time_match = date_time_pattern.search(log_line)
    date_time_str = date_time_match.group(1) if date_time_match else None
    log_date_format = "%d.%m.%Y %H:%M:%S"

    # Parse the date and time string into a datetime object
    if date_time_str:
        log_datetime = datetime.strptime(date_time_str, log_date_format)
        print(f"{GAMER_USERNAME} - {log_datetime}")
    else:
        print("Datetime not found in the log line.")


def main():
  needed_dates = get_needed_dates()
  for link in get_text_files_links(needed_dates):
    extract_login_logout_dates(gamers_login_logout_messages(link))


if __name__ == "__main__":
  main()

