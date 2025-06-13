import re
from datetime import datetime
from data.load_csv_save_db import load_csv_save_mysql


def parse_contributors(contributor_list):
    contributors = []

    for entry in contributor_list:
        match = re.match(r"(.+?)\((.+?)\)", entry.strip())
        if match:
            name = match.group(1).strip()
            role = match.group(2).strip()
            contributors.append({"name": name, "role": role})
        else:
            contributors.append({"name": entry.strip(), "role": "기타"})
    return contributors


if __name__ == "__main__":
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"data/aladin_{today}.csv"
    load_csv_save_mysql(parse_contributors, file_path)
