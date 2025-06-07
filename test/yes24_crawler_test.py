import unittest
from crawler.yes24_crawler import fetch_yes24_bestsellers
import os
import pandas as pd
from datetime import datetime


class TestYes24Crawler(unittest.TestCase):
    def test_csv_created(self):
        fetch_yes24_bestsellers()
        today = datetime.today().strftime("%Y-%m-%d")
        path = f"data/yes24_{today}.csv"
        self.assertTrue(os.path.exists(path))

        df = pd.read_csv(path)
        self.assertGreater(len(df), 0)
        self.assertIn("title", df.columns)
        self.assertIn("author", df.columns)


if __name__ == "__main__":
    unittest.main()
