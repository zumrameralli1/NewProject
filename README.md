# Kitap Öneri Uygulaması

Bu proje, MIS 441 Advanced Programming dersinin final projesi için hazırlanmış basit bir Python web uygulamasıdır.

## Çalıştırma

Terminalde proje klasörüne girip şu komutlardan birini çalıştırın:

```bash
python app.py
```

veya:

```bash
py app.py
```

Sonra tarayıcıda şu adresi açın:

```text
http://127.0.0.1:8000
```

## Özellikler

- Kitap, yazar, tür ve anahtar kelimeye göre arama
- Puana, yıla veya başlığa göre sıralama
- Seçilen kitaba göre içerik tabanlı öneri sistemi
- Basit API endpointleri:
  - `/api/books`
  - `/api/recommend?book_id=1`
- SQLite veritabanına kayıt ve veritabanından okuma
- Multithread destekli Python HTTP server
- Cache kullanılan öneri hesaplama fonksiyonu

## Syllabus ile Bağlantı

- Python programlama: Uygulama Python ile yazıldı.
- Searching and sorting: Arama ve sıralama fonksiyonları eklendi.
- API development: Uygulama JSON dönen API endpointlerine sahip.
- Database integration: Kitaplar SQLite veritabanında tutulur.
- Recommendation systems: İçerik tabanlı öneri sistemi kullanıldı.
- Performance optimization: Öneri fonksiyonunda cache kullanıldı.
- Parallel/concurrent programming: `ThreadingHTTPServer` aynı anda birden fazla isteği karşılayabilir.
- Design pattern yaklaşımı: Öneri mantığı `ContentBasedRecommender` sınıfı içinde ayrı tutuldu.
