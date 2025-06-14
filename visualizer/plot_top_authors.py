import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db.db_connector import get_engine


def visualize_top_authors(df):
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="freq", y="author", palette="Blues_d")
    plt.title("누적 등장 횟수가 많은 저자 TOP 5")
    plt.xlabel("책 수")
    plt.ylabel("저자")
    plt.tight_layout()
    plt.show()


def main():
    engine = get_engine()

    file_path = f"analysis/top_author.sql"
    sql = open(file_path, "r", encoding="utf-8").read()
    df = pd.read_sql(sql, engine)

    visualize_top_authors(df)


if __name__ == "__main__":
    main()
