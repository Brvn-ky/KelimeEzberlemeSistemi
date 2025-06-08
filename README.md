
# 🎯 6 Seferlik Kelime Ezberleme Sistemi

Bu proje, kullanıcıların İngilizce kelimeleri ezberlemesini sağlayan Flask tabanlı bir web uygulamasıdır.  
Kelimeler 6 adımlı bir tekrar algoritması ile öğrenilir.  
Özellikler arasında Quiz sistemi, LLM kelime önerisi, Wordle/Word Chain oyunları, PDF raporlama ve mobil APK desteği yer almaktadır.  
**Bu proje bir ekip çalışması ile geliştirilmiştir.**

## 🔗 GitHub Repo Linki

[https://github.com/Brvn-ky/KelimeEzberlemeSistemi](https://github.com/Brvn-ky/KelimeEzberlemeSistemi)

## Kullanılan Teknolojiler
- Python (Flask)
- HTML/CSS + JavaScript
- SQLite
- SonarQube
- HTML2PDF / wkhtmltopdf
- Android WebView (opsiyonel)


## 🔧 Gereksinimler

- Python 3.10+
- pip
- Flask
- Android Studio (mobil için)

## 💻 Uygulamayı Çalıştırma

1. Gerekli modülleri kur:

```bash
pip install -r requirements.txt
```

2. Flask sunucusunu başlat:

```bash
flask run --host=0.0.0.0
```

3. Tarayıcıdan aç:

```
http://localhost:5000
```

---

## 📁 Modüller – Projenin Yapısı

- `register / login / logout` → Kullanıcı sistemi  
- `add_word` → Yeni kelime ekleme (örnek cümle + görsel)  
- `quiz` → 6 sefer algoritmalı quiz  
- `progress` → Öğrenme süreci tablosu  
- `llm_suggest` → HuggingFace LLM ile öneri  
- `wordle` → 5 harfli Wordle oyunu  
- `word_chain` → Zincirleme kelime oyunu  
- `chart / report` → Matplotlib grafiği ve PDF raporu  
- `settings` → Quiz ayarları (kelime sayısı)  
- `CSV/PDF export` → Verileri dışa aktarma

---

## 📲 Mobil Sürüm

Uygulama `WebView` ile Android’e port edilmiştir.

- WebView üzerinden Flask IP’sine bağlanır (aynı ağda olmalı)  
- `APK` dosyası `app-debug.apk` altında yer alır

---

## 🔍 Test Edilenler

- Kullanıcı oluşturma ve giriş  
- Kelime ekleme + görsel + cümle  
- Quiz döngüsü ve 6 tekrar seviyesi  
- LLM kelime üretimi (Transformers)  
- Oyunlar ve zaman limitleri  
- PDF/CSV çıktıları  
- Mobil uyumluluk (Android Studio)

---


## 👥 Katkıda Bulunanlar

- **Berivan Koçyiğit:** Kullanıcı sistemi (register/login/logout), şifre sıfırlama, temel doğrulama , Mobil APK denemesi
- **Tuğba Avcı:** Kelime ekleme modülü, Quiz ayarları, PDF raporlama, ayarlar sayfası,SonarQube entegrasyonu 
- **Gaye Kaymak:** Quiz sistemi, öğrenme seviyesi takibi, Wordle ve Word Chain oyunları, LLM entegrasyonu 



---
