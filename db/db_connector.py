from sqlalchemy import create_engine


def get_engine():
    user = "root"
    password = "1234"
    host = "localhost"
    dbname = "book_crawling"

    url = f"mysql+pymysql://{user}:{password}@{host}/{dbname}"
    engine = create_engine(url)
    return engine
