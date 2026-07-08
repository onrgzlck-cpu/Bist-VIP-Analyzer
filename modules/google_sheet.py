# modules/google_sheet.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_sheet_client():
    """Google Sheets bağlantısını kurar."""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def update_spreadsheet(data_list):
    """
    data_list: [{'Sembol': 'THYAO', 'Fiyat': 280, 'Sinyal': 'AL'}, ...]
    şeklinde bir liste bekler.
    """
    try:
        client = get_sheet_client()
        sheet = client.open_by_key(config.GOOGLE_SHEET_KEY).sheet1
        
        # Önceki verileri temizle ve başlıkları yaz
        sheet.clear()
        headers = ["Sembol", "Fiyat", "RSI", "Sinyal"]
        sheet.append_row(headers)
        
        # Verileri satır satır ekle
        for item in data_list:
            row = [item.get('Sembol'), item.get('Fiyat'), item.get('RSI'), item.get('Sinyal')]
            sheet.append_row(row)
        
        return True
    except Exception as e:
        print(f"Sheets güncelleme hatası: {e}")
        return False
