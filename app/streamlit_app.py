
import streamlit as st
import requests
import pandas as pd
from gtts import gTTS
from deep_translator import GoogleTranslator

def speak(text, lang_code):
    try:
        # translate text
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
    except:
        translated = text  # fallback

    tts = gTTS(text=translated, lang=lang_code)
    tts.save("voice.mp3")
    return "voice.mp3"
def tr(text):
    try:
        return GoogleTranslator(source='auto', target=get_lang_code(language)).translate(text)
    except:
        return text

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Smart Soil Advisor", layout="centered")

# ================= LANGUAGE =================
# Language mapping (English → Native Script)
languages = {
    "English": "English",
    "Hindi": "हिंदी",
    "Kannada": "ಕನ್ನಡ",
    "Tamil": "தமிழ்",
    "Telugu": "తెలుగు",
    "Malayalam": "മലയാളം",
    "Marathi": "मराठी",
    "Bengali": "বাংলা",
    "Gujarati": "ગુજરાતી",
    "Punjabi": "ਪੰਜਾਬੀ"
}

# Show native names in dropdown
selected_lang_display = st.selectbox(
    "🌐 Language",
    list(languages.values())
)

# Convert back to English key
reverse_languages = {v: k for k, v in languages.items()}
language = reverse_languages[selected_lang_display]

# ================= CSS =================
st.markdown("""
<style>
body {
    background-color: #8E5D26;
}
.card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    margin: 5px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}
.card ul {
    text-align: left;
    padding-left: 20px;
}
.title {
    font-size: 30px;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #6D4C41;
    margin-bottom: 20px;
}
.crop-box {
    background-color: #E8F5E9;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}
.section {
    font-size: 20px;
    font-weight: bold;
    margin-top: 25px;
    color: #1B5E20;
}

/* Fertilizer headings (Chemical & Organic) */
.subhead {
    font-size: 16px;   /* smaller size */
    font-weight: normal;  /* remove bold */
    color: #1B5E20;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f'<div class="title">🌾 {tr("Smart Soil Advisor")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{tr("Check your soil & get crop suggestion")}</div>', unsafe_allow_html=True)

# ================= REFRESH =================
refresh = st.button("🔄 " + tr("Refresh Data"))

# ================= FETCH =================
def get_data():
    try:
        res = requests.get("http://127.0.0.1:8000/sensor")
        return res.json()
    except:
        return {"error": "Backend not running"}

if "data" not in st.session_state or refresh:
    st.session_state.data = get_data()

data = st.session_state.data

if "error" in data:
    st.error(data["error"])
    st.stop()

# ================= SAFE VALUES =================
N = data.get("N", 0)
P = data.get("P", 0)
K = data.get("K", 0)

temp = data.get("temperature", 0)
humidity = data.get("humidity", 0)
rain = data.get("rainfall", 0)

crop = data.get("crop", "Unknown")

imbalance = data.get("imbalance", {})
chem = data.get("chemical_fertilizer", [])
organic = data.get("organic_fertilizer", [])
alt = data.get("alternative_crops", [])

def get_border(val):
    if val < 30:
        return "3px solid red"
    elif val < 70:
        return "3px solid orange"
    else:
        return "3px solid green"
        
def get_lang_code(lang):
    return {
        "English":"en",
        "Hindi":"hi",
        "Kannada":"kn",
        "Tamil":"ta",
        "Telugu":"te",
        "Malayalam":"ml",
        "Marathi":"mr",
        "Bengali":"bn",
        "Gujarati":"gu",
        "Punjabi":"pa"
    }.get(lang, "en")

# ================= SOIL & WEATHER =================
st.markdown(f'<div class="section">{tr("Soil Data")}</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.markdown(f'''
<div class="card" style="background-color:#E8F5E9; border:{get_border(N)};">
N<br><b>{N}</b>
</div>
''', unsafe_allow_html=True)

c2.markdown(f'''
<div class="card" style="background-color:#E3F2FD; border:{get_border(P)};">
P<br><b>{P}</b>
</div>
''', unsafe_allow_html=True)

c3.markdown(f'''
<div class="card" style="background-color:#F3E5F5; border:{get_border(K)};">
K<br><b>{K}</b>
</div>
''', unsafe_allow_html=True)

st.markdown(f'<div class="section">{tr("Weather Data")}</div>', unsafe_allow_html=True)
c4, c5, c6 = st.columns(3)
c4.markdown(f'<div class="card">🌡️ Temp<br><b>{temp}°C</b></div>', unsafe_allow_html=True)
c5.markdown(f'<div class="card">💧 Humidity<br><b>{humidity}%</b></div>', unsafe_allow_html=True)
c6.markdown(f'<div class="card">🌧️ Rain<br><b>{rain} mm</b></div>', unsafe_allow_html=True)

# ================= CROP =================
st.markdown(f'<div class="section">🌾 {tr("Recommended Crop")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="crop-box">➡️ {crop.upper()}</div>', unsafe_allow_html=True)
if st.button("🔊 " + tr("Speak Result")):

    message = f"The best crop for your soil is {crop}"

    audio_file = speak(message, get_lang_code(language))

    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, format="audio/mp3")

# ================= STATUS =================
st.markdown(f'<div class="section">⚠️ {tr("Soil Status")}</div>', unsafe_allow_html=True)

def get_status(val):
    if val < 30:
        return "🔴 Low"
    elif val < 70:
        return "🟡 Medium"
    else:
        return "🟢 Good"

st.write(f"**Nitrogen(N):** {get_status(N)}")
st.write(f"**Phosphorus(P):** {get_status(P)}")
st.write(f"**Potassium(K):** {get_status(K)}")

# ================= FERTILIZER =================
st.markdown(f'<div class="section">🌿 {tr("What To Add")}</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    chem_list = "".join([f"<li>{f}</li>" for f in chem]) if chem else f"<li>{tr('No recommendation')}</li>"
    
    st.markdown(f"""
    <div class="card" style="background-color:#E8F5E9;">
        <b>💊 {tr("Chemical")}</b>
        <ul>
            {chem_list}
        </ul>
    </div>
    """, unsafe_allow_html=True) 

with col2:
    org_list = "".join([f"<li>{f}</li>" for f in organic]) if organic else f"<li>{tr('No recommendation')}</li>"
    
    st.markdown(f"""
    <div class="card" style="background-color:#FFF3E0;">
        <b>🌱 {tr("Organic")}</b>
        <ul>
            {org_list}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ================= ALTERNATIVE CROPS =================
st.markdown(f'<div class="section">🌿 {tr("Other Suitable Crops")}</div>', unsafe_allow_html=True)

if alt:
    for crop_name, score in alt:
       
        st.markdown(f"🌾 **{crop_name}**")
else:
    st.write(tr("No alternative crops available"))

# ================= MANUAL =================
st.markdown(f'<div class="section">🔍 {tr("Check Crop Nutrient Requirement")}</div>', unsafe_allow_html=True)

df = pd.read_csv("crop_dataset.csv")

crop_name = st.text_input(tr("Enter crop name"))

if st.button(tr("Check Requirement")):

    crop_df = df[df["label"].str.lower() == crop_name.lower()]

    if crop_df.empty:
        st.error(tr("Crop not found"))
    else:
        st.success(f"Ideal Nutrient Range for {crop_name}")

        st.write("Nitrogen(N):", crop_df["N"].min(), "to", crop_df["N"].max())
        st.write("Phosphorus(P):", crop_df["P"].min(), "to", crop_df["P"].max())
        st.write("Potassium(K):", crop_df["K"].min(), "to", crop_df["K"].max())

