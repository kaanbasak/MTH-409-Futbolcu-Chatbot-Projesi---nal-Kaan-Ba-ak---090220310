import os
import pandas as pd

def get_metrics(results_file='evaluation_results.csv'):
    """
    evaluation_results.csv dosyasını okur ve kayıtlı sonuçlardan
    Precision, Recall ve F1 skorlarını anlık olarak hesaplar.
    """
    
    # 1. Dosya kontrolü: Henüz test yapılmadıysa bilgi dön.
    if not os.path.exists(results_file):
        return pd.DataFrame([{
            "Durum": "Test Verisi Yok",
            "Bilgi": "Lütfen 'Değerlendirme Paneli'nden testi çalıştırın."
        }])

    try:
        # CSV dosyasını oku (Boş değerleri doldur)
        df = pd.read_csv(results_file).fillna("")
        
        summary_data = []
        models = ["xAI", "Gemini"]

        for model in models:
            # Sütun adlarını belirle (örn: xai_status, gemini_status)
            status_col = f"{model.lower()}_status"
            
            # Eğer CSV'de bu sütun yoksa (eski dosya olabilir), atla
            if status_col not in df.columns:
                continue

            # TP, FP, FN sayılarını filtreleyerek bul
            tp = len(df[df[status_col] == 'TP'])
            fp = len(df[df[status_col] == 'FP'])
            fn = len(df[df[status_col] == 'FN'])

            # Precision Hesapla: TP / (TP + FP)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0

            # Recall Hesapla: TP / (TP + FN)
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

            # F1 Score Hesapla
            if (precision + recall) > 0:
                f1 = 2 * (precision * recall) / (precision + recall)
            else:
                f1 = 0.0

            summary_data.append({
                "Model": model,
                "Precision": round(precision, 2),
                "Recall": round(recall, 2),
                "F1 Score": round(f1, 2)
            })
        
        return pd.DataFrame(summary_data)

    except Exception as e:
        return pd.DataFrame([{"Hata": f"Metrikler okunurken hata oluştu: {str(e)}"}])

if __name__ == "__main__":
    # Test amaçlı çalıştırma
    print(get_metrics())


