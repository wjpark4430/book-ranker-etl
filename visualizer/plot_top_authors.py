import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
from db.db_connector import get_engine
from utils.logger import setup_logger


def visualize_top_authors(df):
    log = setup_logger("plot_top_authors")

    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="freq", y="author", palette="Blues_d")
    plt.title("누적 등장 횟수가 많은 저자 TOP 5")
    plt.xlabel("책 수")
    plt.ylabel("저자")
    plt.tight_layout()

    today = date.today().isoformat()

    output_dir = "plots/top5_trends"
    output_file = f"{output_dir}/{today}.png"

    try:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(output_file, bbox_inches="tight")
        log.info(f"누적 등장 횟수가 많은 저자 TOP 5 시각화 저장 완료: {output_file}")
    except Exception as e:
        log.error(f"[누적 등장 횟수가 많은 저자 TOP 5 시각화 저장 오류] {e}")


def main():
    engine = get_engine()

    file_path = f"analysis/top_author.sql"
    sql = open(file_path, "r", encoding="utf-8").read()
    df = pd.read_sql(sql, engine)

    visualize_top_authors(df)


if __name__ == "__main__":
    main()
