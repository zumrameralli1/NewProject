from functools import lru_cache

class ContentBasedRecommender:
    """Simple content-based recommendation engine for books."""

    def __init__(self, books):
        self.books = books
        self.books_by_id = {book["id"]: book for book in books}

    def search_books(self, query):
        query = query.strip().lower()
        if not query:
            return self.books

        return [
            book
            for book in self.books
            if query in book["title"].lower()
            or query in book["author"].lower()
            or any(query in genre for genre in book["genres"])
            or any(query in keyword for keyword in book["keywords"])
        ]

    def sort_books(self, books, sort_by):
        if sort_by == "year":
            return sorted(books, key=lambda book: book["year"], reverse=True)
        if sort_by == "title":
            return sorted(books, key=lambda book: book["title"])
        return sorted(books, key=lambda book: book["rating"], reverse=True)

    @lru_cache(maxsize=128)
    def recommend(self, favorite_book_id, limit=5):
        favorite = self.books_by_id.get(favorite_book_id)
        if not favorite:
            return []

        scored_books = []
        for book in self.books:
            if book["id"] == favorite_book_id:
                continue

            score = self._similarity_score(favorite, book)
            scored_books.append({**book, "score": round(score, 2)})

        scored_books.sort(key=lambda book: (book["score"], book["rating"]), reverse=True)
        return scored_books[:limit]

    def _similarity_score(self, first_book, second_book):
        first_genres = set(first_book["genres"])
        second_genres = set(second_book["genres"])
        first_keywords = set(first_book["keywords"])
        second_keywords = set(second_book["keywords"])

        genre_score = len(first_genres & second_genres) * 2
        keyword_score = len(first_keywords & second_keywords)
        rating_score = second_book["rating"] / 5

        return genre_score + keyword_score + rating_score
