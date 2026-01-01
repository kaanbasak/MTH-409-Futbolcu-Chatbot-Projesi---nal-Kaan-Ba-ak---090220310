import streamlit as st
import os
import sys
import pandas as pd
import random

# Add project root to sys.path to allow imports from utils and models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_loader import DataLoader
from utils.metrics import get_metrics
from utils.evaluation import Evaluator
from models.xai_handler import XAIHandler
from models.gemini_handler import GeminiHandler

# ---------------------------------------------------------
# 1. KAYNAK YÜKLEME FONKSİYONU (Eksik olan kısım burasıydı)
# ---------------------------------------------------------
@st.cache_resource
def get_resources():
    data_loader = DataLoader()
    xai_handler = XAIHandler()
    gemini_handler = GeminiHandler()
    return data_loader, xai_handler, gemini_handler

# ---------------------------------------------------------
# 2. SOHBET YÖNETİMİ (Selam/Veda)
# ---------------------------------------------------------
def handle_social_intents(text):
    text = text.lower().strip()
    
    # Selamlama
    greetings = ["merhaba", "selam", "slm", "günaydın", "iyi akşamlar", "hey", "merhabalar"]
    if any(text == g for g in greetings) or any(text.startswith(g + " ") for g in greetings):
        return random.choice([
            "Merhaba! Ben Futbolcu Scout Asistanı. Size hangi oyuncu hakkında bilgi verebilirim?",
            "Selamlar! Bir futbolcu arıyorsanız doğru yerdesiniz.",
            "Merhaba! Analiz etmemi istediğiniz bir futbolcu var mı?"
        ])

    # Vedalaşma
    farewells = ["güle güle", "görüşürüz", "baybay", "bye", "iyi geceler", "hoşçakal", "çıkış"]
    if any(f in text for f in farewells):
        return random.choice([
            "Görüşmek üzere! Futbol dolu günler dilerim.",
            "Hoşçakalın, yine beklerim!",
            "İyi günler! Başka bir oyuncu analizi için her zaman buradayım."
        ])
        
    # Teşekkür
    thanks = ["teşekkürler", "teşekkür", "sağ ol", "eyvallah"]
    if any(t in text for t in thanks):
        return "Rica ederim! Yardımcı olabildiysem ne mutlu."

    return None

# ---------------------------------------------------------
# 3. ANA UYGULAMA AKIŞI
# ---------------------------------------------------------

# Önce kaynakları yükle
data_loader, xai_handler, gemini_handler = get_resources()

st.set_page_config(page_title="Futbolcu Scout Asistanı", page_icon="⚽", layout="wide")
st.title("⚽ Futbolcu Scout Asistanı")

# Sekmeler
tab1, tab2 = st.tabs(["💬 Sohbet", "📊 Değerlendirme Paneli (Eval)"])

with tab1:
    # Sidebar
    st.sidebar.title("Sohbet Ayarları")
    model_choice = st.sidebar.radio("Model Seçimi", ["xAI (Grok)", "Gemini"], key="chat_model")

    if st.sidebar.button("Metrikleri Göster (Mock)"):
        metrics = get_metrics()
        st.sidebar.subheader("Performans Metrikleri (Mock)")
        st.sidebar.table(metrics)

    # Chat Interface History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Geçmiş mesajları göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcı girdisi
    if prompt := st.chat_input("Futbolcu hakkında bir soru sorun (örn: Messi hangi takımda?)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Düşünüyor...")
            
            # --- SOSYAL NİYET KONTROLÜ ---
            social_response = handle_social_intents(prompt)
            
            if social_response:
                response = social_response
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            else:
                # --- VERİTABANI SORGUSU ---
                player_info = data_loader.find_player_in_text(prompt)
                
                # Fallback
                if not player_info:
                     player_info = data_loader.get_player_info(prompt)

                if player_info:
                    player_context = str(player_info)
                    
                    if model_choice == "xAI (Grok)":
                        response = xai_handler.generate_response(prompt, player_context)
                    else:
                        response = gemini_handler.generate_response(prompt, player_context)
                        
                    message_placeholder.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    # Bulunamadı / Reddetme mesajı
                    response = (
                        "Üzgünüm, veritabanımda bu isimde bir oyuncu bulamadım veya sorunuzu anlayamadım. "
                        "Ben sadece **futbolcu analizi** ve **scout** verileri üzerine uzmanlaşmış bir asistanım. "
                        "Lütfen bir futbolcu ismi giriniz."
                    )
                    message_placeholder.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.header("Model Performans Değerlendirmesi")
    st.markdown("""
    Bu panel, `data/test_dataset.csv` içindeki soru setini kullanarak her iki modeli de test eder.
    Cevapların doğruluğu, beklenen anahtar kelimelerin (Takım, Mevki vb.) cevap içinde geçip geçmediğine göre kontrol edilir.
    """)
    
    if st.button("Testi Başlat"):
        evaluator = Evaluator()
        
        with st.spinner("Testler çalıştırılıyor (xAI ve Gemini)... Lütfen bekleyin."):
            summary_df, details_df = evaluator.run_evaluation()
            
        st.success("Test tamamlandı!")
        
        # Metrics Table
        st.subheader("1. Karşılaştırma Tablosu")
        st.table(summary_df)
        
        # Charts
        st.subheader("2. Metrik Grafikleri")
        st.bar_chart(summary_df.set_index("Model")[["Precision", "Recall", "F1 Score"]])
        
        # Logs
        st.subheader("3. Detaylı Soru-Cevap Logları")
        st.dataframe(details_df, use_container_width=True)
        
        # Save results
        details_df.to_csv("evaluation_results.csv", index=False)
        st.caption("Sonuçlar 'evaluation_results.csv' dosyasına kaydedildi.")