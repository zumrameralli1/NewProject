# Kitap Öneri Uygulaması

## Proje Amacı

Bu projenin amacı, kullanıcının sevdiği bir kitaba göre benzer kitaplar önerebilen basit bir web uygulaması geliştirmektir.

Uygulama Python ile geliştirilmiştir ve MIS 441 Advanced Programming dersindeki temel konuları göstermek için tasarlanmıştır.

## Problem

Kullanıcılar çok sayıda kitap arasından kendilerine uygun olanı seçmekte zorlanabilir.

Bu uygulama, seçilen kitabın türleri ve anahtar kelimelerini analiz ederek kullanıcıya benzer kitaplar önerir.

## Kullanılan Teknolojiler

- Python
- HTML, CSS, JavaScript
- Python `http.server`
- SQLite
- JSON API
- İçerik tabanlı öneri yaklaşımı

## Uygulama Özellikleri

- Kitap listesi görüntüleme
- Kitap, yazar, tür ve anahtar kelimeye göre arama
- Kitapları puana, yıla veya başlığa göre sıralama
- Kullanıcının seçtiği kitaba göre öneri üretme
- API üzerinden veri gönderme

## Syllabus Konuları ile Eşleşme

| Syllabus Konusu | Projede Karşılığı |
| --- | --- |
| Python Programming | Backend Python ile yazıldı |
| Searching Algorithms | Kitap arama fonksiyonu kullanıldı |
| Sorting Algorithms | Kitaplar puan, yıl ve başlığa göre sıralanıyor |
| API Development | `/api/books` ve `/api/recommend` endpointleri var |
| Database Integration | Kitaplar SQLite veritabanına kaydedilip oradan okunuyor |
| Recommendation Systems | İçerik tabanlı öneri sistemi kullanıldı |
| Performance Optimization | Öneri fonksiyonunda cache kullanıldı |
| Parallel Programming | `ThreadingHTTPServer` ile çoklu istek desteği var |
| Design Patterns | Öneri sistemi ayrı bir sınıf olarak tasarlandı |

## Öneri Sistemi Nasıl Çalışır?

Uygulamadaki her kitap şu bilgilere sahiptir:

- Başlık
- Yazar
- Türler
- Anahtar kelimeler
- Puan
- Yayın yılı

Kullanıcı bir kitap seçtiğinde sistem:

1. Seçilen kitabın türlerini ve anahtar kelimelerini alır.
2. Diğer kitaplarla ortak tür ve anahtar kelime sayısını hesaplar.
3. Kitabın puanını da skora ekler.
4. En yüksek skora sahip kitapları öneri olarak listeler.

## Benzerlik Skoru

Benzerlik skoru şu mantıkla hesaplanır:

```text
skor = ortak tür sayısı * 2 + ortak anahtar kelime sayısı + kitap puanı / 5
```

Tür eşleşmelerine daha fazla ağırlık verilmiştir çünkü kitap önerisinde tür bilgisi daha belirleyicidir.

## API Yapısı

### Kitapları Listeleme

```text
GET /api/books
```

Arama ve sıralama parametreleri:

```text
GET /api/books?q=python&sort=rating
```

### Öneri Alma

```text
GET /api/recommend?book_id=1
```

Bu endpoint seçilen kitaba benzer kitapları JSON formatında döndürür.

## Kod Yapısı

| Dosya | Açıklama |
| --- | --- |
| `app.py` | Web server, API endpointleri ve arayüz |
| `recommender.py` | Arama, sıralama ve öneri algoritması |
| `database.py` | SQLite veritabanı işlemleri |
| `data.py` | Kitap veri seti |
| `README.md` | Kurulum ve kullanım açıklaması |
| `sunum.md` | Proje sunumu için içerik |

## Sonuç

Bu proje, küçük ölçekli bir kitap öneri uygulaması geliştirerek derste işlenen temel konuları uygulamalı şekilde göstermektedir.

Uygulama basit tutulmuştur ancak API, arama, sıralama, cache, sınıf yapısı ve öneri algoritması gibi syllabus kapsamındaki ihtiyaçları karşılamaktadır.
