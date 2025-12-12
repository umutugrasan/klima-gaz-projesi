import streamlit as st
import streamlit.components.v1 as components

# 1. HTML Kodunu bir değişkene atayın (Size verdiğim uzun HTML kodu)
# Not: HTML kodundaki 'const API_KEY = "";' satırını olduğu gibi bırakın, Python ile değiştireceğiz.
html_code = """
<!DOCTYPE html>
<html lang="tr">
...
    <script>
        // API Configuration
        const API_KEY = ""; // Burası boş kalabilir, aşağıda Python ile dolduracağız
...
</html>
"""

# 2. Streamlit Secrets'tan anahtarı çekin
# Eğer secrets tanımlı değilse hata vermemesi için try-except veya .get kullanılabilir
try:
    my_api_key = st.secrets["GEMINI_API_KEY"]
except FileNotFoundError:
    my_api_key = "" # Lokal çalışırken hata almamak için (secrets.toml yoksa)
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets ayarlarını yapın.")

# 3. HTML içindeki boş API anahtarını, gerçek anahtarla değiştirin
# Bu işlem Python tarafında gerçekleşir, GitHub'daki kodunuzda anahtar görünmez.
final_html = html_code.replace('const API_KEY = "";', f'const API_KEY = "{my_api_key}";')

# 4. Sayfayı tam ekran olarak göster
st.set_page_config(layout="wide")
components.html(final_html, height=800, scrolling=True)
