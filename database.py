import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Books table (now includes 'book_copy_id')
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                quantity INTEGER DEFAULT 1 CHECK (quantity >= 1),
                book_copy_id TEXT UNIQUE
            )
        """)
        
        # Borrowed books (added 'extended_return_date')
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrowed_books (
                id INTEGER PRIMARY KEY,
                book_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                borrow_date TEXT NOT NULL,
                return_date TEXT,
                extended_return_date TEXT,
                returned INTEGER DEFAULT 0,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        """)
        self.conn.commit()

    def add_book(self, title, author, quantity=1):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1!")
        self.cursor.execute(
            "INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
            (title, author, quantity)
        )
        self.conn.commit()

    def borrow_book(self, book_id, user_id):
        # Check if book exists and is available
        self.cursor.execute("SELECT quantity FROM books WHERE id=?", (book_id,))
        result = self.cursor.fetchone()
        if not result:
            raise ValueError("Book not registered!")
        if result[0] <= 0:
            raise ValueError("Book out of stock!")

        # Auto-set borrow date to today
        borrow_date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            "INSERT INTO borrowed_books (book_id, user_id, borrow_date) VALUES (?, ?, ?)",
            (book_id, user_id, borrow_date)
        )
        self.conn.commit()