# main.py
import logging
from modules import bist_data, indicators, google_sheet

# Loglama ayarı
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_pipeline():
    logging.info("🚀 Analiz motoru başlatılıyor...")
    
    # 1. Verileri Çek
    raw_data = bist_data.get_all_bist_data()
    results = []
    
    # 2. İşle ve Sinyalleri Oluştur
    for ticker, df in raw_data.items():
        df_with_indicators = indicators.calculate_indicators(df)
        signal = indicators.generate_signal(df_with_indicators)
        
        # Sonuçları listeye ekle
        current_price = df['Close'].iloc[-1]
        results.append({
            "Sembol": ticker.replace(".IS", ""),
            "Fiyat": round(float(current_price), 2),
            "RSI": round(float(df_with_indicators['RSI'].iloc[-1]), 2),
            "Sinyal": signal
        })
    
    # 3. Google Sheets'e Yazdır
    logging.info("💾 Google Sheets güncelleniyor...")
    if google_sheet.update_spreadsheet(results):
        logging.info("✅ İşlem başarıyla tamamlandı.")
    else:
        logging.error("❌ Google Sheets güncellemesi başarısız!")

if __name__ == "__main__":
    run_pipeline()
