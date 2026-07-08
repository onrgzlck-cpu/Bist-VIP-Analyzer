# modules/indicators.py
import pandas as pd
import pandas_ta as ta

def calculate_indicators(df):
    """
    Verilen DataFrame üzerine teknik indikatörleri ekler.
    """
    if df is None or df.empty:
        return None

    # RSI (14 günlük)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    
    # Hareketli Ortalamalar (EMA 5, EMA 20, SMA 200)
    df['EMA5'] = ta.ema(df['Close'], length=5)
    df['EMA20'] = ta.ema(df['Close'], length=20)
    df['SMA200'] = ta.sma(df['Close'], length=200)
    
    # MACD
    macd = ta.macd(df['Close'])
    df = pd.concat([df, macd], axis=1)
    
    # ATR (Volatilite takibi için)
    df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
    
    return df

def generate_signal(df):
    """
    Hesaplanan indikatörlere göre basit bir AL/SAT sinyali üretir.
    """
    if df is None or 'RSI' not in df.columns:
        return "VERİ_YOK"
    
    last_row = df.iloc[-1]
    
    # Örnek Sinyal Mantığı (Bunu ileride daha da profesyonelleştireceğiz)
    if last_row['RSI'] < 40 and last_row['Close'] > last_row['EMA20']:
        return "AL_SINYALI"
    elif last_row['RSI'] > 70:
        return "SAT_SINYALI"
    else:
        return "TUT"
