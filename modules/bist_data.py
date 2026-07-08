# modules/bist_data.py
import yfinance as yf
import pandas as pd
import os
import sys
import logging

# Proje kök dizinini sisteme ekle (config'e ulaşabilmek için)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Loglama ayarı
logging.basicConfig(level=logging.INFO)

def load_tickers():
    """BIST listesini config dosyasından okur."""
    if not os.path.exists(config.BIST_LIST_PATH):
        logging.error(f"Hata: {config.BIST_LIST_PATH} bulunamadı!")
        return []
    with open(config.BIST_LIST_PATH, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def get_bist_data(ticker):
    """Belirtilen hisse için veriyi çeker ve temizler."""
    try:
        data = yf.download(ticker, period="6mo", interval=config.TIMEFRAME, progress=False)
        if data.empty:
            return None
        
        # MultiIndex sütunlarını düzelt (yfinance bazen karmaşık veri yapısı döner)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)
            
        return data
    except Exception as e:
        logging.error(f"{ticker} verisi alınırken hata oluştu: {e}")
        return None

def get_all_bist_data():
    """Tüm listeyi tarar ve sözlük yapısında döner."""
    tickers = load_tickers()
    all_data = {}
    logging.info(f"{len(tickers)} adet hisse taranıyor...")
    
    for ticker in tickers:
        df = get_bist_data(ticker)
        if df is not None:
            all_data[ticker] = df
    
    return all_data
