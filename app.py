import streamlit as st
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Bağlantısı
def get_data():
    # GitHub Secrets'tan JSON verisini al
    creds_json = os.environ.get("CREDENTIALS_JSON")
    if not creds_json:
        st.error("CREDENTIALS_JSON bulunamadı! Lütfen Streamlit Secrets ayarlarını kontrol edin.")
        return pd.DataFrame()
    
    # JSON verisini sözlüğe çevir
    creds_dict = json.loads(creds_json)
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(os.environ.get("GOOGLE_SHEET_KEY")).sheet1
    return pd.DataFrame(sheet.get_all_records())

st.set_page_config(page_title="BIST Analiz Paneli", layout="wide")
st.title("📊 BIST VIP Analiz Paneli")

if st.button("Verileri Yenile"):
    df = get_data()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        # Basit Görselleştirme
        st.subheader("RSI Dağılımı")
        st.bar_chart(df.set_index("Sembol")["RSI"])
    else:
        st.warning("Veri bulunamadı veya Sheets boş.")
