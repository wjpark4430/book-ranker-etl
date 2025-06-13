import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db.db_connector import get_engine


def visualize_date_first(df):
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.figure(figsize=(12, 6))
    sns.stripplot(data=df, x="date_added", y="title", palette="Set2")
    plt.title("날짜별 랭킹 1위 도서")
    plt.xlabel("날짜")
    plt.ylabel("도서 제목")
    plt.tight_layout()
    plt.show()


def main():
    engine = get_engine()

    file_path = f"analysis/date_first_yes24.sql"
    sql = open(file_path, "r", encoding="utf-8").read()
    df = pd.read_sql(sql, engine)

    visualize_date_first(df)


if __name__ == "__main__":
    main()
