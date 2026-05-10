import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from database import initialize_database, load_books
from recommender import ContentBasedRecommender


HOST = "127.0.0.1"
PORT = 8000
BOOKS = []
recommender = None


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
  <title>Kitap Öneri Uygulaması</title>
  <style>
    :root {{
      --bg: #f6f7f2;
      --ink: #1f2933;
      --muted: #65758b;
      --line: #d8ded2;
      --accent: #2f7d6d;
      --accent-strong: #225f54;
      --card: #ffffff;
      --warm: #e9b872;
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
      font-size: clamp(28px, 4vw, 46px);
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
    <h1>Kitap Öneri Uygulaması</h1>
    <p>Python ile geliştirilmiş basit bir öneri sistemi. Kitapları arar, sıralar ve seçilen kitaba benzer kitapları içerik tabanlı filtreleme ile önerir.</p>
  </header>

  <main>
    <section class="panel controls">
      <label>
        Kitap, yazar, tür veya anahtar kelime ara
        <input id="searchInput" type="search" placeholder="Örn: python, fantasy, Orwell">
      </label>
      <label>
        Sıralama
        <select id="sortSelect">
          <option value="rating">Puana göre</option>
          <option value="year">Yeniye göre</option>
          <option value="title">Başlığa göre</option>
        </select>
      </label>
      <button id="searchButton">Ara</button>
    </section>

    <section class="panel">
      <label>
        Sevdiğin kitabı seç
        <select id="favoriteSelect">
          {options}
        </select>
      </label>
      <button id="recommendButton" style="margin-top: 12px;">Öneri Getir</button>
    </section>

    <section class="layout">
      <div class="panel">
        <h2>Kitap Listesi</h2>
        <div id="books" class="book-list"></div>
      </div>
      <div class="panel">
        <h2>Önerilen Kitaplar</h2>
        <div id="recommendations" class="book-list">
          <div class="empty">Bir kitap seçip öneri getir.</div>
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
            ${{book.author}} · ${{book.year}} · Puan: ${{book.rating}}<br>
            Türler: ${{book.genres.join(", ")}}<br>
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
      renderList(booksElement, books, "Sonuç bulunamadı.");
    }}

    async function loadRecommendations() {{
      const response = await fetch(`/api/recommend?book_id=${{favoriteSelect.value}}`);
      const books = await response.json();
      renderList(recommendationsElement, books, "Bu kitap için öneri bulunamadı.");
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
    global BOOKS, recommender

    initialize_database()
    BOOKS = load_books()
    recommender = ContentBasedRecommender(BOOKS)

    server = ThreadingHTTPServer((HOST, PORT), BookRecommendationHandler)
    print(f"Kitap öneri uygulaması çalışıyor: http://{HOST}:{PORT}")
    print("Durdurmak için Ctrl+C")
    server.serve_forever()


if __name__ == "__main__":
    main()
