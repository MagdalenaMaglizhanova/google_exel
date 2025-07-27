import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Конфигурация за Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "your_credentials.json"  # Името на вашия JSON файл
SHEET_NAME = "Учители"  # Име на вашия Google Sheet

# Аутентикация
def authenticate_google_sheets():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)
    return client

# Зареждане на данни от Sheets
def load_teachers_data(client):
    sheet = client.open(SHEET_NAME).sheet1  # Първият лист
    data = sheet.get_all_records()  # Взима всички редове като речници
    return data

# Streamlit UI
st.title("📊 Анализ на учителите")
st.markdown("**Филтриране на учители над 40 години**")

# Зареждане на данни
try:
    client = authenticate_google_sheets()
    teachers = load_teachers_data(client)
    
    # Филтриране
    teachers_over_40 = [teacher for teacher in teachers if int(teacher["Години"]) > 40]
    
    # Показване на резултатите
    st.write(f"### Общ брой учители: {len(teachers)}")
    st.write(f"### Учители над 40 години: {len(teachers_over_40)}")
    
    if teachers_over_40:
        st.dataframe(teachers_over_40)
    else:
        st.warning("Няма учители над 40 години.")
        
except Exception as e:
    st.error(f"Грешка при зареждане на данните: {e}")
