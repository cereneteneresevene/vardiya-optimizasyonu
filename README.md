# 🏥 Çalışan Vardiya Optimizasyonu

Bir hastanenin haftalık hemşire vardiya planını otomatik olarak oluşturan optimizasyon sistemi.

## 📌 Problem Tanımı

Hastanelerde vardiya planlaması manuel yapıldığında zaman alıcı ve hata prone bir süreçtir.
Bu proje, kısıtları otomatik olarak karşılayan en iyi vardiya planını matematiksel optimizasyon ile üretir.

## 🎯 Amaç

Kıdemli hemşireleri gece vardiyasına daha az atayarak iş yükünü dengeli dağıtmak.

## 📐 Kısıtlar

- Her vardiyada minimum hemşire sayısı karşılanmalı (sabah: 3, öğlen: 3, gece: 2)
- Hemşire izin gününde çalışamaz
- Haftalık maksimum çalışma saati aşılamaz
- Bir hemşire günde yalnızca 1 vardiyada çalışabilir

## 🔧 Kullanılan Teknolojiler

- Python 3.14
- Pandas — veri işleme
- PuLP — matematiksel optimizasyon
- Streamlit — web arayüzü

## 🚀 Kurulum

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Çalıştırma

```bash
# Veri üret
python3 veri_uret.py

# Modeli çalıştır
python3 model.py

# Arayüzü aç
streamlit run app.py
```

## 📁 Proje Yapısı

```
vardiya_optimizasyonu/
├── data/              → CSV dosyaları
├── veri_uret.py       → Sentetik veri üretimi
├── model.py           → Optimizasyon modeli
├── app.py             → Streamlit arayüzü
└── requirements.txt   → Bağımlılıklar
```