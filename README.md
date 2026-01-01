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

⚙️ Kurulum ve Çalıştırma
Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

1. Projeyi Klonlayın

Bash
git clone [https://github.com/KULLANICI_ADINIZ/futbol-scout-asistani.git](https://github.com/KULLANICI_ADINIZ/futbol-scout-asistani.git)
cd futbol-scout-asistani
2. Sanal Ortam Oluşturun (Önerilen)

Bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Gerekli Kütüphaneleri Yükleyin

Bash
pip install -r requirements.txt
4. .env Dosyasını Ayarlayın

Proje ana dizininde .env adında bir dosya oluşturun ve API anahtarlarınızı ekleyin:

Plaintext
GOOGLE_API_KEY="Sizin_Google_Gemini_Keyiniz"
XAI_API_KEY="Sizin_xAI_Grok_Keyiniz"
5. Uygulamayı Başlatın

Bash
streamlit run app.py
