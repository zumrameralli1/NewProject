import json
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


HOST = "127.0.0.1"
PORT = 8000


BOOKS = [
    {
        "id": 1,
        "title": "Dune",
        "author": "Frank Herbert",
        "genres": ["science fiction", "adventure", "politics"],
        "keywords": ["desert", "empire", "strategy", "ecology"],
        "rating": 4.8,
        "year": 1965,
    },
    {
        "id": 2,
        "title": "Foundation",
        "author": "Isaac Asimov",
        "genres": ["science fiction", "history", "strategy"],
        "keywords": ["empire", "prediction", "civilization", "science"],
        "rating": 4.6,
        "year": 1951,
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "genres": ["dystopia", "politics", "classic"],
        "keywords": ["surveillance", "state", "freedom", "propaganda"],
        "rating": 4.7,
        "year": 1949,
    },
    {
        "id": 4,
        "title": "Animal Farm",
        "author": "George Orwell",
        "genres": ["classic", "politics", "satire"],
        "keywords": ["power", "revolution", "society", "allegory"],
        "rating": 4.4,
        "year": 1945,
    },
    {
        "id": 5,
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "genres": ["fantasy", "adventure", "classic"],
        "keywords": ["journey", "dragon", "friendship", "quest"],
        "rating": 4.8,
        "year": 1937,
    },
    {
        "id": 6,
        "title": "The Fellowship of the Ring",
        "author": "J. R. R. Tolkien",
        "genres": ["fantasy", "adventure", "classic"],
        "keywords": ["quest", "friendship", "ring", "war"],
        "rating": 4.9,
        "year": 1954,
    },
    {
        "id": 7,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J. K. Rowling",
        "genres": ["fantasy", "young adult", "adventure"],
        "keywords": ["magic", "school", "friendship", "mystery"],
        "rating": 4.7,
        "year": 1997,
    },
    {
        "id": 8,
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "genres": ["fantasy", "adventure", "drama"],
        "keywords": ["magic", "music", "school", "legend"],
        "rating": 4.6,
        "year": 2007,
    },
    {
        "id": 9,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genres": ["romance", "classic", "drama"],
        "keywords": ["family", "society", "marriage", "wit"],
        "rating": 4.5,
        "year": 1813,
    },
    {
        "id": 10,
        "title": "Jane Eyre",
        "author": "Charlotte Bronte",
        "genres": ["romance", "classic", "drama"],
        "keywords": ["independence", "mystery", "identity", "love"],
        "rating": 4.4,
        "year": 1847,
    },
    {
        "id": 11,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genres": ["philosophy", "adventure", "self improvement"],
        "keywords": ["dreams", "journey", "purpose", "destiny"],
        "rating": 4.2,
        "year": 1988,
    },
    {
        "id": 12,
        "title": "Atomic Habits",
        "author": "James Clear",
        "genres": ["self improvement", "psychology", "productivity"],
        "keywords": ["habits", "goals", "systems", "behavior"],
        "rating": 4.8,
        "year": 2018,
    },
    {
        "id": 13,
        "title": "Deep Work",
        "author": "Cal Newport",
        "genres": ["productivity", "technology", "self improvement"],
        "keywords": ["focus", "work", "attention", "career"],
        "rating": 4.5,
        "year": 2016,
    },
    {
        "id": 14,
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "genres": ["psychology", "science", "business"],
        "keywords": ["decision", "bias", "mind", "thinking"],
        "rating": 4.6,
        "year": 2011,
    },
    {
        "id": 15,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "genres": ["technology", "programming", "software"],
        "keywords": ["code", "quality", "design", "maintenance"],
        "rating": 4.7,
        "year": 2008,
    },
    {
        "id": 16,
        "title": "Fluent Python",
        "author": "Luciano Ramalho",
        "genres": ["programming", "technology", "python"],
        "keywords": ["python", "advanced", "functions", "objects"],
        "rating": 4.7,
        "year": 2015,
    },
    {
        "id": 17,
        "title": "Automate the Boring Stuff with Python",
        "author": "Al Sweigart",
        "genres": ["programming", "python", "automation"],
        "keywords": ["python", "files", "scraping", "automation"],
        "rating": 4.6,
        "year": 2015,
    },
    {
        "id": 18,
        "title": "The Girl with the Dragon Tattoo",
        "author": "Stieg Larsson",
        "genres": ["mystery", "crime", "thriller"],
        "keywords": ["investigation", "crime", "journalism", "secrets"],
        "rating": 4.4,
        "year": 2005,
    },
]


class ContentBasedRecommender:
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


recommender = ContentBasedRecommender(BOOKS)


class BookRecommendationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/":
            self._send_html(self._page())
            return

        if parsed_url.path == "/api/books":
            query_params = parse_qs(parsed_url.query)
            query = query_params.get("q", [""])[0]
            sort_by = query_params.get("sort", ["rating"])[0]
            books = recommender.search_books(query)
            books = recommender.sort_books(books, sort_by)
            self._send_json(books)
            return

        if parsed_url.path == "/api/recommend":
            query_params = parse_qs(parsed_url.query)
            book_id = int(query_params.get("book_id", ["0"])[0])
            results = recommender.recommend(book_id)
            self._send_json(results)
            return

        self.send_error(404, "Page not found")

    def log_message(self, format, *args):
        return

    def _send_html(self, html):
        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, data):
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _page(self):
        options = "\n".join(
            f'<option value="{book["id"]}">{book["title"]} - {book["author"]}</option>'
            for book in BOOKS
        )
        return f"""<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kitap Oneri Uygulamasi</title>
  <style>
    :root {{
      --bg: #f6f7f2;
      --ink: #1f2933;
      --muted: #65758b;
      --line: #d8ded2;
      --accent: #2f7d6d;
      --accent-strong: #225f54;
      --card: #ffffff;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
    }}

    header {{
      background: #21312f;
      color: white;
      padding: 28px max(20px, 8vw);
    }}

    header h1 {{
      margin: 0 0 8px;
      font-size: clamp(28px, 4vw, 44px);
      letter-spacing: 0;
    }}

    header p {{
      margin: 0;
      color: #d7e1dc;
      max-width: 760px;
      line-height: 1.5;
    }}

    main {{
      width: min(1120px, calc(100% - 32px));
      margin: 24px auto 48px;
      display: grid;
      gap: 18px;
    }}

    .panel {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}

    .controls {{
      display: grid;
      grid-template-columns: 1.3fr 1fr auto;
      gap: 12px;
      align-items: end;
    }}

    label {{
      display: grid;
      gap: 6px;
      font-size: 14px;
      color: var(--muted);
    }}

    input, select, button {{
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 0 12px;
      font-size: 15px;
      background: white;
      color: var(--ink);
    }}

    button {{
      border-color: var(--accent);
      background: var(--accent);
      color: white;
      cursor: pointer;
      font-weight: 700;
    }}

    button:hover {{ background: var(--accent-strong); }}

    .layout {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }}

    h2 {{
      margin: 0 0 14px;
      font-size: 22px;
      letter-spacing: 0;
    }}

    .book-list {{
      display: grid;
      gap: 10px;
    }}

    .book {{
      border: 1px solid var(--line);
      border-left: 5px solid var(--accent);
      border-radius: 8px;
      padding: 12px;
      background: #fbfcfa;
    }}

    .book strong {{
      display: block;
      margin-bottom: 5px;
      font-size: 16px;
    }}

    .meta {{
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }}

    .score {{
      display: inline-block;
      margin-top: 8px;
      padding: 4px 8px;
      border-radius: 999px;
      background: #fff4d9;
      color: #795200;
      font-size: 13px;
      font-weight: 700;
    }}

    .empty {{
      color: var(--muted);
      border: 1px dashed var(--line);
      border-radius: 8px;
      padding: 18px;
      background: #fbfcfa;
    }}

    @media (max-width: 820px) {{
      .controls, .layout {{ grid-template-columns: 1fr; }}
      button {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Kitap Oneri Uygulamasi</h1>
    <p>Recommendation Systems konusu icin hazirlanan basit bir content-based filtering uygulamasi.</p>
  </header>

  <main>
    <section class="panel controls">
      <label>
        Kitap, yazar, tur veya anahtar kelime ara
        <input id="searchInput" type="search" placeholder="Orn: python, fantasy, Orwell">
      </label>
      <label>
        Siralama
        <select id="sortSelect">
          <option value="rating">Puana gore</option>
          <option value="year">Yeniye gore</option>
          <option value="title">Basliga gore</option>
        </select>
      </label>
      <button id="searchButton">Ara</button>
    </section>

    <section class="panel">
      <label>
        Sevdigin kitabi sec
        <select id="favoriteSelect">
          {options}
        </select>
      </label>
      <button id="recommendButton" style="margin-top: 12px;">Oneri Getir</button>
    </section>

    <section class="layout">
      <div class="panel">
        <h2>Kitap Listesi</h2>
        <div id="books" class="book-list"></div>
      </div>
      <div class="panel">
        <h2>Onerilen Kitaplar</h2>
        <div id="recommendations" class="book-list">
          <div class="empty">Bir kitap secip oneri getir.</div>
        </div>
      </div>
    </section>
  </main>

  <script>
    const booksElement = document.querySelector("#books");
    const recommendationsElement = document.querySelector("#recommendations");
    const searchInput = document.querySelector("#searchInput");
    const sortSelect = document.querySelector("#sortSelect");
    const favoriteSelect = document.querySelector("#favoriteSelect");

    function renderBook(book) {{
      const score = book.score === undefined ? "" : `<span class="score">Benzerlik skoru: ${{book.score}}</span>`;
      return `
        <article class="book">
          <strong>${{book.title}}</strong>
          <div class="meta">
            ${{book.author}} - ${{book.year}} - Puan: ${{book.rating}}<br>
            Turler: ${{book.genres.join(", ")}}<br>
            Anahtar kelimeler: ${{book.keywords.join(", ")}}
          </div>
          ${{score}}
        </article>
      `;
    }}

    function renderList(element, books, emptyText) {{
      element.innerHTML = books.length
        ? books.map(renderBook).join("")
        : `<div class="empty">${{emptyText}}</div>`;
    }}

    async function loadBooks() {{
      const params = new URLSearchParams({{
        q: searchInput.value,
        sort: sortSelect.value
      }});
      const response = await fetch(`/api/books?${{params}}`);
      const books = await response.json();
      renderList(booksElement, books, "Sonuc bulunamadi.");
    }}

    async function loadRecommendations() {{
      const response = await fetch(`/api/recommend?book_id=${{favoriteSelect.value}}`);
      const books = await response.json();
      renderList(recommendationsElement, books, "Bu kitap icin oneri bulunamadi.");
    }}

    document.querySelector("#searchButton").addEventListener("click", loadBooks);
    document.querySelector("#recommendButton").addEventListener("click", loadRecommendations);
    searchInput.addEventListener("keydown", event => {{
      if (event.key === "Enter") loadBooks();
    }});

    loadBooks();
  </script>
</body>
</html>"""


def main():
    server = HTTPServer((HOST, PORT), BookRecommendationHandler)
    print(f"Kitap oneri uygulamasi calisiyor: http://{HOST}:{PORT}")
    print("Durdurmak icin Ctrl+C")
    server.serve_forever()


if __name__ == "__main__":
    main()
