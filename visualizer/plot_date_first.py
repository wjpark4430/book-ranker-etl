import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
from db.db_connector import get_engine
from utils.logger import setup_logger


def visualize_date_first(df):
    log = setup_logger("plot_date_first")

    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.figure(figsize=(12, 8))
    sns.stripplot(data=df, x="date_added", y="title", palette="Set2", size=7)
    plt.yticks(fontsize=9)
    plt.title("날짜별 랭킹 1위 도서")
    plt.xlabel("날짜")
    plt.ylabel("도서 제목")
    plt.tight_layout()

    today = date.today().isoformat()

    output_dir = "plots/date_first"
    output_file = f"{output_dir}/{today}.png"

    try:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(output_file, bbox_inches="tight")
        log.info(f"날짜별 랭킹 1위 도서 시각화 저장 완료: {output_file}")
    except Exception as e:
        log.error(f"[날짜별 랭킹 1위 도서 시각화 저장 오류] {e}")


def main():
    engine = get_engine()

    file_path = f"analysis/date_first_yes24.sql"
    sql = open(file_path, "r", encoding="utf-8").read()
    df = pd.read_sql(sql, engine)

    visualize_date_first(df)


if __name__ == "__main__":
    main()
