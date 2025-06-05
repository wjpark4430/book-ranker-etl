CREATE TABLE IF NOT EXISTS book_rank (
    id INT PRIMARY KEY,
    book_rank INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    date_added DATE NOT NULL,
    UNIQUE KEY unique_book (title, date_added)
);


