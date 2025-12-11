import streamlit as st
import streamlit.components.v1 as components

# Sayfa ayarını geniş yapalım ki HTML rahat görünsün
st.set_page_config(layout="wide", page_title="Klima Gaz Kaçağı Projesi")

# index.html dosyasını oku
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# HTML'i ekrana bas (Yükseklik değerini içeriğe göre artırabilirsiniz)
components.html(html_code, height=1200, scrolling=True)