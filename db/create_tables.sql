CREATE TABLE IF NOT EXISTS book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    price INT NOT NULL
);
CREATE TABLE IF NOT EXISTS book_rank (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    book_rank INT NOT NULL,
    date_added DATE NOT NULL,
    FOREIGN KEY (book_id) REFERENCES book(id) UNIQUE KEY unique_book (book_id, date_added)
);
CREATE TABLE IF NOT EXISTS person (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS contribute (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    book_id INT NOT NULL,
    book_role VARCHAR(255) NOT NULL,
    FOREIGN KEY (person_id) REFERENCES person(id),
    FOREIGN KEY (book_id) REFERENCES book(id)
);