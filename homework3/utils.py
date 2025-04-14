from datetime import datetime
import csv
import re


def read_dict_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def is_valid_date(date_str, pattern):
    try:
        datetime.strptime(date_str, pattern)
        return True
    except ValueError:
        return False