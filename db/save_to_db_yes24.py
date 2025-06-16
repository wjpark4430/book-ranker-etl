import re
from datetime import datetime
from data.load_csv_save_db import load_csv_save_mysql


def parse_contributors(raw_text):
    contributors = []

    for part in raw_text.split("/"):
        match = re.match(r"(.+?)(저|역|글그림|그림|글|감수)$", part.strip())
        if match:
            name = match.group(1).strip()
            role = match.group(2).strip()
            contributors.append({"name": name, "role": role})
        else:
            contributors.append({"name": part.strip(), "role": "기타"})
    return contributors


if __name__ == "__main__":
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"data/yes24_{today}.csv"
    load_csv_save_mysql(parse_contributors, file_path)
