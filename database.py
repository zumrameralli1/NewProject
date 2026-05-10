import json
import sqlite3
from pathlib import Path

from data import BOOKS


DATABASE_PATH = Path(__file__).with_name("books.db")


def initialize_database():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genres TEXT NOT NULL,
                keywords TEXT NOT NULL,
                rating REAL NOT NULL,
                year INTEGER NOT NULL
            )
            """
        )
        connection.execute("DELETE FROM books")
        connection.executemany(
            """
            INSERT INTO books (id, title, author, genres, keywords, rating, year)
            VALUES (:id, :title, :author, :genres, :keywords, :rating, :year)
            """,
            [_serialize_book(book) for book in BOOKS],
        )


def load_books():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, title, author, genres, keywords, rating, year
            FROM books
            ORDER BY id
            """
        ).fetchall()
    return [_deserialize_book(row) for row in rows]


def _serialize_book(book):
    return {
        **book,
        "genres": json.dumps(book["genres"]),
        "keywords": json.dumps(book["keywords"]),
    }


def _deserialize_book(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "author": row["author"],
        "genres": json.loads(row["genres"]),
        "keywords": json.loads(row["keywords"]),
        "rating": row["rating"],
        "year": row["year"],
    }
