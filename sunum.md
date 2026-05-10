# Kitap Oneri Uygulamasi

## Proje Amaci

Bu projenin amaci, kullanicinin sevdigi bir kitaba gore benzer kitaplar onerebilen basit bir web uygulamasi gelistirmektir.

Uygulama Python ile gelistirilmistir ve MIS 441 Advanced Programming dersindeki **Recommendation Systems** konusu icin hazirlanmistir.

## Problem

Kullanicilar cok sayida kitap arasindan kendilerine uygun olani secmekte zorlanabilir.

Bu uygulama, secilen kitabin turleri ve anahtar kelimelerini analiz ederek kullaniciya benzer kitaplar onerir.

## Kullanilan Teknolojiler

- Python
- HTML, CSS, JavaScript
- Python `http.server`
- Icerik tabanli oneri yaklasimi

## Uygulama Ozellikleri

- Kitap listesi goruntuleme
- Kitap, yazar, tur ve anahtar kelimeye gore arama
- Kullanicinin sectigi kitaba gore oneri uretme
- Onerilen kitaplari benzerlik skoruna gore listeleme

## Secilen Syllabus Konusu

Bu projede syllabus icinden **Recommendation Systems** konusu secilmistir.

Proje, recommendation systems basligi altinda gecen **content-based filtering** yaklasimini kullanir.

## Oneri Sistemi Nasil Calisir?

Uygulamadaki her kitap su bilgilere sahiptir:

- Baslik
- Yazar
- Turler
- Anahtar kelimeler
- Puan
- Yayin yili

Kullanici bir kitap sectiginde sistem:

1. Secilen kitabin turlerini ve anahtar kelimelerini alir.
2. Diger kitaplarla ortak tur ve anahtar kelime sayisini hesaplar.
3. Kitabin puanini da skora ekler.
4. En yuksek skora sahip kitaplari oneri olarak listeler.

## Benzerlik Skoru

Benzerlik skoru su mantikla hesaplanir:

```text
skor = ortak tur sayisi * 2 + ortak anahtar kelime sayisi + kitap puani / 5
```

Tur eslesmelerine daha fazla agirlik verilmistir cunku kitap onerisinde tur bilgisi daha belirleyicidir.

## Kod Yapisi

| Dosya | Aciklama |
| --- | --- |
| `app.py` | Veri seti, oneri algoritmasi, web server ve arayuz |
| `README.md` | Kurulum ve kullanim aciklamasi |
| `sunum.md` | Proje sunumu icin icerik |

## Sonuc

Bu proje, kucuk olcekli bir kitap oneri uygulamasi gelistirerek **Recommendation Systems** konusunu uygulamali sekilde gostermektedir.

Uygulama basit tutulmustur ve ana odak secilen kitaba gore benzer kitap onerisi uretmektir.
