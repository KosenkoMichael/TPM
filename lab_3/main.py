import csv
import json
import re

import checksum


telephone_pattern = r"^\+7\-\(\d{3}\)\-\d{3}\-\d{2}\-\d{2}$"
height_pattern = r"^([1-2]\.\d{2}|3\.00)$"
inn_pattern = r"^\d{12}$"
identifier_pattern = r"^\d{2}-\d{2}/\d{2}$"
occupation_pattern = r"^[A-Za-zА-Яа-яёЁ\s-]+$"
latitude_pattern = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$"
blood_type_pattern = r"^(A|B|AB|O)[\u2212+]$"
issn_pattern = r"^\d{4}-\d{4}$"
uuid_pattern = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
date_pattern = r"^(?:19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"

patterns = []
patterns.append(telephone_pattern)
patterns.append(height_pattern)
patterns.append(inn_pattern)
patterns.append(identifier_pattern)
patterns.append(occupation_pattern)
patterns.append(latitude_pattern)
patterns.append(blood_type_pattern)
patterns.append(issn_pattern)
patterns.append(uuid_pattern)
patterns.append(date_pattern)


def row_check(row):
    for i in range(10):
        if not re.match(patterns[i], row[i]):
            return False
    return True


def control_sum_sount(result):
    return checksum.calculate_checksum(result)


def csv_check(file_path):
    result = []
    with open(file_path, mode='r', newline='', encoding="utf-16") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        for i, row in enumerate(reader, start=0):
            if not row_check(row):
                result.append(i)
    return result


def result_serialize(string, path):
    result = {
        "variant": "40",
        "checksum": f"{string}"
    }
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)


result_serialize(control_sum_sount(csv_check("40.csv")), "result.json")
