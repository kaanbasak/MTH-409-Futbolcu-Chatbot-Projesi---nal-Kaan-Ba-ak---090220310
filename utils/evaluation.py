import pandas as pd
import time
import numpy as np
from utils.data_loader import DataLoader
from models.xai_handler import XAIHandler
from models.gemini_handler import GeminiHandler

class Evaluator:
    def __init__(self, test_file='data/test_dataset.csv'):
        # NaN değerleri boş string ile dolduruyoruz ki "nan" metni aramayalım
        self.test_df = pd.read_csv(test_file).fillna("")
        self.data_loader = DataLoader()
        self.xai_handler = XAIHandler()
        self.gemini_handler = GeminiHandler()

    def run_evaluation(self):
        results = []
        
        # Metrik sayaçları (TP: Doğru, FP: Yanlış Bilgi, FN: Bulunamadı/Cevapsız)
        metrics = {
            "xAI": {"tp": 0, "fp": 0, "fn": 0, "response_times": []},
            "Gemini": {"tp": 0, "fp": 0, "fn": 0, "response_times": []}
        }

        print(f"Toplam {len(self.test_df)} test sorusu işleniyor...")

        for index, row in self.test_df.iterrows():
            question = row['question']
            intent = row.get('intent', 'General') # Intent sütunu yoksa varsayılan
            
            # Beklenen değerleri string'e çevir ve küçük harf yap
            expected_vals = {
                "team": str(row['expected_team']).lower().strip(),
                "position": str(row['expected_position']).lower().strip(),
                "player": str(row['expected_player']).lower().strip()
            }
            
            # 1. Veri Arama (Retrieval)
            player_info = self.data_loader.find_player_in_text(question)
            if not player_info:
                 player_info = self.data_loader.get_player_info(question)

            player_context = str(player_info) if player_info else "Veri bulunamadı"
            
            # --- Modelleri Test Etme Fonksiyonu ---
            def evaluate_model(handler, model_name):
                start_time = time.time()
                
                # Cevap Üretimi
                if player_info:
                    response = handler.generate_response(question, player_context)
                else:
                    response = "Veri bulunamadı."
                
                duration = time.time() - start_time
                metrics[model_name]["response_times"].append(duration)
                
                # Doğruluk Kontrolü
                status = self._check_correctness_detailed(response, expected_vals, intent)
                
                if status == "TP":
                    metrics[model_name]["tp"] += 1
                elif status == "FN":
                    metrics[model_name]["fn"] += 1
                else: # FP
                    metrics[model_name]["fp"] += 1
                    
                return response, status

            # xAI Çalıştır
            xai_resp, xai_status = evaluate_model(self.xai_handler, "xAI")
            
            # Gemini Çalıştır
            gemini_resp, gemini_status = evaluate_model(self.gemini_handler, "Gemini")

            # Sonuçları Kaydet
            results.append({
                "question": question,
                "intent": intent,
                "expected_team": expected_vals["team"],
                "xai_response": xai_resp,
                "xai_status": xai_status, # TP, FP, FN
                "gemini_response": gemini_resp,
                "gemini_status": gemini_status
            })

        return self._calculate_final_metrics(metrics), pd.DataFrame(results)

    def _check_correctness_detailed(self, response, expected_vals, intent):
        """
        Daha hassas kontrol mekanizması.
        Dönüş Değerleri: 'TP' (Doğru), 'FP' (Yanlış/Halüsinasyon), 'FN' (Bulunamadı)
        """
        response = response.lower()
        
        # 1. Model cevabı bulamadıysa (Retrieval Failure veya Model Failure) -> FN
        fail_phrases = ["veri bulunamadı", "bilgi yok", "bilinmiyor", "eşleşen oyuncu yok", "üzgünüm"]
        # Eğer cevap çok kısaysa ve olumsuz kelimeler içeriyorsa
        if len(response) < 50 and any(phrase in response for phrase in fail_phrases):
            return "FN"

        is_correct = False
        
        # 2. Intent'e göre kontrol
        if intent == "Ask_Team":
            # Takım adı boş değilse ve cevapta geçiyorsa
            if expected_vals["team"] and expected_vals["team"] in response:
                is_correct = True
                
        elif intent == "Ask_Position":
            # Mevki adı boş değilse ve cevapta geçiyorsa
            if expected_vals["position"] and expected_vals["position"] in response:
                is_correct = True
                
        elif intent == "Ask_Info":
            # Genel bilgide oyuncu adı ve en az bir beklenen bilgi (takım veya mevki) geçmeli
            has_player = expected_vals["player"] in response
            has_detail = (expected_vals["team"] in response) or (expected_vals["position"] in response)
            
            # Sadece uzunluk değil, içerik kontrolü
            if has_player and has_detail:
                is_correct = True

        else:
            # Fallback: Takım veya Mevki geçiyor mu?
            if (expected_vals["team"] and expected_vals["team"] in response) or \
               (expected_vals["position"] and expected_vals["position"] in response):
                is_correct = True

        # Sonuç Kararı
        if is_correct:
            return "TP"
        else:
            # Cevap verdi ama beklenen kelime yok -> Yanlış Bilgi (FP)
            return "FP"

    def _calculate_final_metrics(self, metrics):
        final_metrics = []
        
        for model_name, data in metrics.items():
            tp = data["tp"]
            fp = data["fp"]
            fn = data["fn"]
            
            # Precision = TP / (TP + FP)  -> Model konuştuğunda ne kadar doğru?
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            
            # Recall = TP / (TP + FN)     -> Modelin toplam soruları bilme oranı ne?
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            # F1 Score
            if (precision + recall) > 0:
                f1 = 2 * (precision * recall) / (precision + recall)
            else:
                f1 = 0.0
                
            avg_time = sum(data["response_times"]) / len(data["response_times"]) if data["response_times"] else 0
            
            final_metrics.append({
                "Model": model_name,
                "Precision": round(precision, 2),
                "Recall": round(recall, 2),
                "F1 Score": round(f1, 2),
                "Avg Time (s)": round(avg_time, 2),
                "TP": tp,
                "FP": fp,
                "FN": fn
            })
            
        return pd.DataFrame(final_metrics)