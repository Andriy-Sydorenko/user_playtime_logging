import re
from datetime import datetime, timedelta
from typing import IO

import customtkinter as ctk


def set_default_appearance_mode(default_value: str):
    if default_value == "Dark mode":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")


def extract_datetime_from_log_string(log_string: str, log_date_format: str):
    date_time_pattern = re.compile(r'\[(.*?)\]')  # noqa
    date_time_match = date_time_pattern.search(log_string)
    date_time_str = date_time_match.group(1) if date_time_match else None
    datetime_obj = datetime.strptime(date_time_str, log_date_format)
    return datetime_obj


def timedelta_to_str(td: timedelta):
    days, seconds = divmod(td.seconds, 86400)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    total_hours = (days * 24) + hours

    formatted_time = "{:02}:{:02}:{:02}".format(total_hours, minutes, seconds)

    return formatted_time


def parse_usernames_from_file(file_path):
    with open(file_path, "r") as file:
        read_file = file.read()
        lines = [line.strip() for line in read_file.split("\n")]
    return lines
