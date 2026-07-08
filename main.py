# main.py
import logging
from modules import bist_data, indicators, google_sheet, telegram_notifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_pipeline():
    logging.info("🚀 Analiz başlatılıyor...")
    
    # 1. Veri çek
    raw_data = bist_data.get_all_bist_data()
    results = []
    
    for ticker, df in raw_data.items():
        df_with_indicators = indicators.calculate_indicators(df)
        signal = indicators.generate_signal(df_with_indicators)
        
        current_price = df['Close'].iloc[-1]
        results.append({
            "Sembol": ticker.replace(".IS", ""),
            "Fiyat": round(float(current_price), 2),
            "RSI": round(float(df_with_indicators['RSI'].iloc[-1]), 2),
            "Sinyal": signal
        })
        
        # 2. Eğer AL sinyali varsa Telegram'a hemen haber ver
        if signal == "AL_SINYALI":
            msg = f"🦅 BIST AL SİNYALİ!\n\n📈 Hisse: {ticker.replace('.IS','')}\n💰 Fiyat: {round(float(current_price), 2)}\n📊 RSI: {round(float(df_with_indicators['RSI'].iloc[-1]), 2)}"
            telegram_notifier.send_telegram_message(msg)

    # 3. Google Sheets güncelle
    google_sheet.update_spreadsheet(results)
    logging.info("✅ İşlem tamamlandı, Telegram ve Sheets güncellendi.")

if __name__ == "__main__":
    run_pipeline()
