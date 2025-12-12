import streamlit as st
import streamlit.components.v1 as components

# Sayfa ayarını geniş yapalım
st.set_page_config(layout="wide", page_title="DİREN Gaz Takip")

# API Anahtarını alalım (Hata verirse boş geçelim)
try:
    my_api_key = st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError):
    my_api_key = "" 
    # Eğer secrets çalışmazsa uyarı vermeden devam et, kullanıcıya chatte hata döner.

# --------------------------------------------------------
# HTML KODU (Python String İçinde)
# --------------------------------------------------------
html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DİREN | Akıllı Gaz Takip Sistemi</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        :root { --primary: #0ea5e9; --secondary: #6366f1; --dark: #0f172a; }
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; color: #334155; }
        h1, h2, h3, h4, h5 { font-family: 'Plus Jakarta Sans', sans-serif; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        .fade-in { animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .glass { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.5); }
        .nav-item.active { background-color: #e0f2fe; color: #0284c7; font-weight: 600; }
        .bubble-user { background: linear-gradient(135deg, #0ea5e9, #2563eb); color: white; border-radius: 16px 16px 0 16px; }
        .bubble-ai { background: white; border: 1px solid #e2e8f0; color: #1e293b; border-radius: 16px 16px 16px 0; }
        .typing-dot { animation: typing 1.4s infinite ease-in-out both; }
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        @keyframes typing { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
    </style>
</head>
<body class="flex flex-col min-h-screen pb-20 md:pb-0">

    <header class="fixed top-0 w-full z-50 glass shadow-sm transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-sky-200">
                    <i class="ri-sensor-line text-xl"></i>
                </div>
                <div>
                    <h1 class="text-lg font-bold text-slate-800 leading-none">DİREN</h1>
                    <p class="text-[10px] uppercase tracking-wider text-slate-500 font-semibold mt-0.5">Gaz Tespit Ar-Ge</p>
                </div>
            </div>
            <nav class="hidden md:flex items-center space-x-1 bg-slate-100/50 p-1 rounded-xl">
                <button onclick="app.nav('overview')" id="d-overview" class="nav-item px-4 py-2 rounded-lg text-sm font-medium text-slate-500 transition-all">Genel Bakış</button>
                <button onclick="app.nav('analysis')" id="d-analysis" class="nav-item px-4 py-2 rounded-lg text-sm font-medium text-slate-500 transition-all">Gaz & Sensör</button>
                <button onclick="app.nav('hardware')" id="d-hardware" class="nav-item px-4 py-2 rounded-lg text-sm font-medium text-slate-500 transition-all">Donanım</button>
                <button onclick="app.nav('software')" id="d-software" class="nav-item px-4 py-2 rounded-lg text-sm font-medium text-slate-500 transition-all">Yazılım & Plan</button>
                <button onclick="app.nav('ai')" id="d-ai" class="ml-2 px-4 py-2 rounded-lg text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-200 transition-all flex items-center gap-2">
                    <i class="ri-sparkling-fill"></i> Asistan
                </button>
            </nav>
        </div>
    </header>

    <main class="flex-grow max-w-7xl mx-auto w-full px-4 pt-24 pb-10 space-y-8">
        <section id="s-overview" class="fade-in space-y-6">
            <div class="bg-slate-900 rounded-3xl p-8 md:p-12 text-white relative overflow-hidden shadow-2xl shadow-slate-200">
                <div class="absolute top-0 right-0 w-96 h-96 bg-sky-500 rounded-full mix-blend-overlay filter blur-3xl opacity-20 -mr-20 -mt-20"></div>
                <div class="relative z-10 max-w-3xl">
                    <h2 class="text-3xl md:text-5xl font-bold mb-6 leading-tight">Yeni Nesil Klima Gazı <br><span class="text-sky-400">Kaçak Tespit Sistemi</span></h2>
                    <p class="text-slate-300 text-lg leading-relaxed mb-8">Üniversite kampüsleri ve kritik altyapılar için R-32 ve R-410A gaz kaçaklarını tespit eden IoT sistemi.</p>
                </div>
            </div>
             <div class="grid md:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                    <h3 class="font-bold text-slate-800 text-lg mb-3 flex items-center gap-2"><i class="ri-alert-fill text-orange-500"></i> Problem: Yanıcılık</h3>
                    <p class="text-slate-600 text-sm">R-32 (A2L) yanıcıdır. Eski sensörler (MQ-135) yetersizdir.</p>
                </div>
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                    <h3 class="font-bold text-slate-800 text-lg mb-3 flex items-center gap-2"><i class="ri-checkbox-circle-fill text-green-500"></i> Çözüm: TGS2630</h3>
                    <p class="text-slate-600 text-sm">Filtreli endüstriyel sensörler ve güvenli donanım kullanılacaktır.</p>
                </div>
            </div>
        </section>

        <section id="s-analysis" class="hidden fade-in space-y-6">
            <div class="flex flex-col md:flex-row gap-6">
                <div class="w-full md:w-1/3 space-y-4">
                    <div class="bg-blue-600 rounded-2xl p-6 text-white shadow-lg">
                        <h3 class="font-bold">Kritik Bilgi</h3>
                        <p class="text-sm text-blue-50 mt-2">Gaz havadan ağırdır. Sensör zemine (30-50 cm) monte edilmelidir.</p>
                    </div>
                </div>
                <div class="w-full md:w-2/3 bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
                    <h3 class="font-bold text-lg text-slate-800 mb-4">Sensör Karşılaştırma</h3>
                    <div class="h-64 w-full mb-6"><canvas id="sensorChart"></canvas></div>
                </div>
            </div>
        </section>

        <section id="s-hardware" class="hidden fade-in space-y-6">
            <div class="grid md:grid-cols-3 gap-6">
                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                    <h4 class="font-bold text-slate-700"><i class="ri-cpu-line text-sky-500"></i> ESP32</h4>
                    <p class="text-xs text-slate-500 mt-2">Wi-Fi ve Bluetooth için gereklidir.</p>
                </div>
                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm relative">
                    <span class="absolute top-3 right-3 flex h-3 w-3"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span><span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span></span>
                    <h4 class="font-bold text-slate-700"><i class="ri-sensor-fill text-green-500"></i> Figaro TGS2600</h4>
                    <p class="text-xs text-slate-500 mt-2 mb-4">R-32 ve hava kalitesi için filtreli sensör.</p>
                    <a href="https://www.ozdisan.com/p/gaz-sensorleri-915/figaro-tgs2600-433747?srsltid=AfmBOopCwS-_tUTd4Q2mtEGaD2QPb7GTyHJdHO-sErfnjeYIxzp-9r9m" target="_blank" class="block w-full py-2 bg-green-600 hover:bg-green-700 text-white text-xs font-bold text-center rounded-lg">Satın Al (Özdisan)</a>
                </div>
                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                    <h4 class="font-bold text-slate-700"><i class="ri-plug-line text-orange-500"></i> Güç & SSR</h4>
                    <p class="text-xs text-slate-500 mt-2">5V 2A Adaptör ve kıvılcım önleyici SSR Röle.</p>
                </div>
            </div>
        </section>

        <section id="s-software" class="hidden fade-in space-y-6">
             <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
                <h3 class="font-bold text-slate-800 text-lg mb-4">12 Haftalık Plan</h3>
                <ul class="space-y-4">
                    <li class="flex gap-3"><span class="font-bold text-sky-500">1-2. Hafta:</span> <span class="text-slate-600 text-sm">Malzeme Tedariği</span></li>
                    <li class="flex gap-3"><span class="font-bold text-slate-500">3-5. Hafta:</span> <span class="text-slate-600 text-sm">Prototip & Test (Çakmak Gazı)</span></li>
                    <li class="flex gap-3"><span class="font-bold text-slate-500">6-9. Hafta:</span> <span class="text-slate-600 text-sm">Mobil App & MQTT</span></li>
                    <li class="flex gap-3"><span class="font-bold text-slate-500">10-12. Hafta:</span> <span class="text-slate-600 text-sm">Saha Kurulumu</span></li>
                </ul>
            </div>
        </section>

        <section id="s-ai" class="hidden fade-in h-[500px] flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden">
            <div id="chat-container" class="flex-grow overflow-y-auto p-4 space-y-4 bg-slate-50">
                <div class="flex gap-3 fade-in">
                    <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 text-xs shrink-0"><i class="ri-robot-2-line"></i></div>
                    <div class="bubble-ai p-3 text-sm max-w-[85%]">Merhaba! Teknik sorularını bekliyorum. (Örn: Voltaj bölücü nasıl yapılır?)</div>
                </div>
            </div>
            <div class="p-4 bg-white border-t border-slate-100 flex gap-2">
                <input type="text" id="user-input" placeholder="Soru sor..." class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none" onkeypress="if(event.key === 'Enter') app.askAI()">
                <button onclick="app.askAI()" id="send-btn" class="bg-indigo-600 text-white rounded-xl px-4"><i class="ri-send-plane-fill"></i></button>
            </div>
        </section>
    </main>

    <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 px-2 py-1 flex justify-between items-center z-50">
        <button onclick="app.nav('overview')" class="flex flex-col items-center p-2"><i class="ri-home-4-line text-xl"></i><span class="text-[9px]">Özet</span></button>
        <button onclick="app.nav('analysis')" class="flex flex-col items-center p-2"><i class="ri-flask-line text-xl"></i><span class="text-[9px]">Gaz</span></button>
        <button onclick="app.nav('ai')" class="-mt-6"><div class="w-12 h-12 bg-indigo-600 rounded-full flex items-center justify-center text-white border-4 border-white"><i class="ri-sparkling-fill"></i></div></button>
        <button onclick="app.nav('hardware')" class="flex flex-col items-center p-2"><i class="ri-cpu-line text-xl"></i><span class="text-[9px]">Donanım</span></button>
        <button onclick="app.nav('software')" class="flex flex-col items-center p-2"><i class="ri-code-s-slash-line text-xl"></i><span class="text-[9px]">Yazılım</span></button>
    </nav>

    <script>
        const API_KEY = ""; // PYTHON TARAFINDAN DOLDURULACAK

        const app = {
            chart: null,
            init: () => {
                app.initChart();
                app.nav('overview');
            },
            nav: (id) => {
                document.querySelectorAll('section').forEach(el => el.classList.add('hidden'));
                document.getElementById(`s-${id}`).classList.remove('hidden');
                window.scrollTo({top: 0});
            },
            initChart: () => {
                const ctx = document.getElementById('sensorChart').getContext('2d');
                app.chart = new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: ['Hassasiyet', 'Seçicilik', 'R-32 Uyumu', 'Maliyet', 'Ömür'],
                        datasets: [
                            { label: 'TGS 2630 (Önerilen)', data: [85, 90, 95, 60, 80], borderColor: '#0ea5e9', backgroundColor: 'rgba(14, 165, 233, 0.2)' },
                            { label: 'MQ-135 (Hobi)', data: [40, 20, 30, 95, 40], borderColor: '#ef4444', backgroundColor: 'rgba(239, 68, 68, 0.2)' }
                        ]
                    },
                    options: { maintainAspectRatio: false }
                });
            },
            addMsg: (text, sender) => {
                const container = document.getElementById('chat-container');
                const div = document.createElement('div');
                div.className = `flex gap-3 fade-in ${sender === 'user' ? 'flex-row-reverse' : ''}`;
                const bubbleClass = sender === 'user' ? 'bubble-user' : 'bubble-ai';
                div.innerHTML = `<div class="${bubbleClass} p-3 text-sm max-w-[85%]">${marked.parse(text)}</div>`;
                container.appendChild(div);
                container.scrollTop = container.scrollHeight;
            },
            askAI: async () => {
                const input = document.getElementById('user-input');
                const query = input.value.trim();
                if(!query) return;
                app.addMsg(query, 'user');
                input.value = '';
                
                if (!API_KEY) {
                    app.addMsg("API Key eksik! Streamlit Secrets ayarını kontrol edin.", 'ai');
                    return;
                }

                try {
                    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${API_KEY}`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            contents: [{ parts: [{ text: query }] }],
                            systemInstruction: { parts: [{ text: "Sen DİREN projesi teknik asistanısın. Kısa ve teknik cevap ver." }] }
                        })
                    });
                    const data = await response.json();
                    app.addMsg(data.candidates?.[0]?.content?.parts?.[0]?.text || "Hata oluştu.", 'ai');
                } catch(e) {
                    app.addMsg("Bağlantı hatası.", 'ai');
                }
            }
        };
        document.addEventListener('DOMContentLoaded', app.init);
    </script>
</body>
</html>
"""
# --------------------------------------------------------
# PYTHON KODU (Inject & Render)
# --------------------------------------------------------

# 1. API Anahtarını HTML içine göm
final_html = html_code.replace('const API_KEY = "";', f'const API_KEY = "{my_api_key}";')

# 2. HTML'i Render et (BURASI ÇOK ÖNEMLİ)
# Yüksekliği 800px veya daha fazla veriyoruz ki ekran bembeyaz kalmasın.
components.html(final_html, height=1000, scrolling=True)
