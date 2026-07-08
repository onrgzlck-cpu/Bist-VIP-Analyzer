# modules/indicators.py (Güncellenmiş Hali)
import pandas as pd
import pandas_ta as ta

def calculate_indicators(df):
    if df is None or df.empty:
        return None
    
    # RSI, EMA ve MACD hesaplamaları...
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['EMA5'] = ta.ema(df['Close'], length=5)
    df['EMA20'] = ta.ema(df['Close'], length=20)
    
    return df

def generate_signal(df):
    # Eğer veri yoksa veya RSI hesaplanamadıysa (NaN ise) hemen çık
    if df is None or 'RSI' not in df.columns or pd.isna(df['RSI'].iloc[-1]):
        return "VERİ_YETERSİZ"
    
    last_row = df.iloc[-1]
    rsi_val = float(last_row['RSI'])
    close_val = float(last_row['Close'])
    ema20_val = float(last_row['EMA20'])
    
    # Artık None değerleri temizledik, güvenle kıyaslayabiliriz
    if rsi_val < 40 and close_val > ema20_val:
        return "AL_SINYALI"
    elif rsi_val > 70:
        return "SAT_SINYALI"
    else:
        return "TUT"
