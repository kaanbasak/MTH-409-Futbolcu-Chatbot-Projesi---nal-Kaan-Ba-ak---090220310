# ⚽ Futbolcu Scout Asistanı (Football Scout Assistant)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange)
![xAI](https://img.shields.io/badge/xAI-Grok-black)

Bu proje, futbolcu verilerini analiz etmek ve kullanıcıların sorularını yanıtlamak için geliştirilmiş **Yapay Zeka Destekli bir Chatbot** uygulamasıdır. 

Uygulama, **Google Gemini** ve **xAI (Grok)** modellerini kullanarak kullanıcı sorularını yanıtlar ve cevap kalitesini ölçmek için özel bir **Değerlendirme (Evaluation) Paneli** içerir.

## 🚀 Özellikler

* **🤖 Çift Model Desteği:** Kullanıcılar **Google Gemini** veya **xAI (Grok)** modelleri arasında seçim yapabilir.
* **🔍 RAG Mimarisi:** Sorulara doğrudan cevap vermek yerine, yerel veri setinden (`test_dataset.csv`) ilgili oyuncu verisini bulur ve modele bağlam (context) olarak verir.
* **💬 Akıllı Sohbet:** Selamlama, vedalaşma ve futbol dışı konuları filtreleme yeteneğine sahiptir.
* **📊 Performans Değerlendirmesi:** Modellerin doğruluğunu (Precision, Recall, F1 Score) ölçen entegre bir test modülü bulunur.
* **📂 Modüler Yapı:** Kod tabanı `models`, `utils` ve `data` olarak ayrıştırılarak temiz bir mimari sunar.

## 🛠️ Kullanılan Teknolojiler

* **Arayüz:** [Streamlit](https://streamlit.io/)
* **LLM Modelleri:** Google Gemini 2.5 Flash & xAI grok-4-latest
* **Veri İşleme:** Pandas, NumPy
* **API Entegrasyonu:** `google-generativeai`, `openai` (xAI uyumlu)

## 📂 Proje Yapısı

```text
futbol-scout-asistani/
├── app.py                  # Ana uygulama dosyası (Streamlit)
├── requirements.txt        # Gerekli kütüphaneler
├── .env                    # API anahtarları (Gizli dosya)
├── data/
│   └── test_dataset.csv    # Oyuncu verileri ve test seti
├── models/
│   ├── gemini_handler.py   # Google Gemini API entegrasyonu
│   └── xai_handler.py      # xAI (Grok) API entegrasyonu
└── utils/
    ├── data_loader.py      # Veri yükleme ve arama fonksiyonları
    ├── evaluation.py       # Model performans ölçüm sistemi
    └── metrics.py          # Metrik hesaplama araçları
