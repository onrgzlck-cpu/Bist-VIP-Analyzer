# modules/google_sheet.py
import json
import tempfile
import config

def get_sheet_client():
    # GitHub Secrets'tan gelen veriyi al
    creds_json = os.environ.get("CREDENTIALS_JSON")
    
    # Geçici bir dosya oluştur
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        tmp.write(creds_json)
        tmp_path = tmp.name
        
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(tmp_path, scope)
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
