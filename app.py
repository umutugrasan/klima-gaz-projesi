import streamlit as st
import streamlit.components.v1 as components

# Sayfa ayarları
st.set_page_config(layout="wide", page_title="DİREN Gaz Takip")

# 1. API Anahtarını al (Hata vermemesi için .get kullanıyoruz)
api_key = st.secrets.get("GEMINI_API_KEY", "")

# 2. Yanındaki 'index.html' dosyasını oku
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# 3. HTML içindeki boş API anahtarını Python'daki gerçek anahtarla değiştir
final_html = html_code.replace('const API_KEY = "";', f'const API_KEY = "{api_key}";')

# 4. Ekrana bas
components.html(final_html, height=1000, scrolling=True)
