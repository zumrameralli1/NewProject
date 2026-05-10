# Kitap Oneri Uygulamasi - Recommendation Systems

Bu proje, MIS 441 Advanced Programming dersindeki **Recommendation Systems** konusu icin hazirlanmis basit bir Python web uygulamasidir.

## Calistirma

Terminalde proje klasorune girip su komutlardan birini calistirin:

```bash
python app.py
```

veya:

```bash
py app.py
```

Sonra tarayicida su adresi acin:

```text
http://127.0.0.1:8000
```

## Ozellikler

- Kitap, yazar, tur ve anahtar kelimeye gore arama
- Secilen kitaba gore icerik tabanli oneri sistemi
- Onerilen kitaplari benzerlik skoruna gore listeleme
- Basit web arayuzu

## Secilen Syllabus Konusu

Bu proje syllabus icinden **Recommendation Systems** basligini secer.

Projede kullanilan yaklasim **content-based filtering** yani icerik tabanli filtrelemedir.

Kullanici bir kitap secer. Sistem, secilen kitabin turleri ve anahtar kelimeleri ile diger kitaplari karsilastirir. Benzerlik skoru yuksek olan kitaplar kullaniciya onerilir.

## Dosya Yapisi

- `app.py`: Veri seti, oneri algoritmasi, web server ve arayuz tek dosyadadir.
- `sunum.md`: Sunum icin hazirlanan markdown dosyasidir.
