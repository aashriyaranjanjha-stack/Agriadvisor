import pandas as pd
import streamlit as st
st.set_page_config(page_title="AgriAdvisor", layout="centered")
from sklearn.tree import DecisionTreeClassifier
from deep_translator import GoogleTranslator

# ---------------- TRANSLATION FUNCTION ----------------
def translate_text(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except:
        return text

# ---------------- LANGUAGES ----------------
lang_codes = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Punjabi": "pa",
    "Bengali": "bn"
}

language = st.selectbox("🌐 Choose Language", list(lang_codes.keys()))

# ---------------- LABELS ----------------
labels = {
    "English": {
        "title": "AgriAdvisor 🌾",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "ph": "pH",
        "rainfall": "Rainfall (mm)",
        "button": "Predict Crop & Fertilizer",
        "crop": "Recommended Crop: ",
        "fert": "Recommended Fertilizer: "
    },

    "Hindi": {
        "title": "एग्रीएडवाइज़र 🌾",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फॉस्फोरस (P)",
        "potassium": "पोटैशियम (K)",
        "temperature": "तापमान (°C)",
        "humidity": "आर्द्रता (%)",
        "ph": "pH",
        "rainfall": "वर्षा (mm)",
        "button": "फसल और उर्वरक बताएं",
        "crop": "सुझाई गई फसल: ",
        "fert": "सुझाया गया उर्वरक: "
    },

    "Kannada": {
        "title": "ಅಗ್ರಿಅಡ್ವೈಸರ್ 🌾",
        "nitrogen": "ನೈಟ್ರಜನ (N)",
        "phosphorus": "ಫಾಸ್ಫರಸ್ (P)",
        "potassium": "ಪೊಟ್ಯಾಸಿಯಮ್ (K)",
        "temperature": "ತಾಪಮಾನ (°C)",
        "humidity": "ಆರ್ದ್ರತೆ (%)",
        "ph": "pH",
        "rainfall": "ಮಳೆ (mm)",
        "button": "ಬೆಳೆ ಮತ್ತು ರಸಗೊಬ್ಬರ ಸೂಚಿಸಿ",
        "crop": "ಸೂಚಿಸಲಾದ ಬೆಳೆ: ",
        "fert": "ಸೂಚಿಸಲಾದ ರಸಗೊಬ್ಬರ: "
    },

    "Punjabi": {
        "title": "ਅਗਰੀਐਡਵਾਇਜ਼ਰ 🌾",
        "nitrogen": "ਨਾਈਟ੍ਰੋਜਨ (N)",
        "phosphorus": "ਫਾਸਫੋਰਸ (P)",
        "potassium": "ਪੋਟਾਸ਼ੀਅਮ (K)",
        "temperature": "ਤਾਪਮਾਨ (°C)",
        "humidity": "ਨਮੀ (%)",
        "ph": "pH",
        "rainfall": "ਵਰਖਾ (mm)",
        "button": "ਫਸਲ ਅਤੇ ਖਾਦ ਦੱਸੋ",
        "crop": "ਸਿਫਾਰਸ਼ੀ ਫਸਲ: ",
        "fert": "ਸਿਫਾਰਸ਼ੀ ਖਾਦ: "
    },

    "Bengali": {
        "title": "অ্যাগ্রিএডভাইজার 🌾",
        "nitrogen": "নাইট্রোজেন (N)",
        "phosphorus": "ফসফরাস (P)",
        "potassium": "পটাশিয়াম (K)",
        "temperature": "তাপমাত্রা (°C)",
        "humidity": "আর্দ্রতা (%)",
        "ph": "pH",
        "rainfall": "বৃষ্টি (mm)",
        "button": "ফসল ও সার বলুন",
        "crop": "প্রস্তাবিত ফসল: ",
        "fert": "প্রস্তাবিত সার: "
    }
}

# ---------------- TITLE ----------------
st.title(labels[language]["title"])

# ---------------- LOAD DATA ----------------
data = pd.read_csv("Crop_recommendation.csv", encoding='latin1')

X = data[['N','P','K','temperature','humidity','ph','rainfall']]
y = data['label']

model = DecisionTreeClassifier()
model.fit(X, y)

# ---------------- FERTILIZER MODEL ----------------

fert_data = pd.read_csv("Fertilizer Prediction.csv", encoding='latin1')

# clean column names
fert_data.columns = fert_data.columns.str.strip()

# INPUT features
X_fert = fert_data[['Temparature','Humidity','Moisture','Nitrogen','Potassium','Phosphorous']]

# OUTPUT
y_fert = fert_data['Fertilizer Name']

# MODEL
fert_model = DecisionTreeClassifier()
fert_model.fit(X_fert, y_fert)

# ---------------- INPUTS ----------------
N = st.number_input(labels[language]["nitrogen"], 0, 140, 90)
P = st.number_input(labels[language]["phosphorus"], 0, 145, 40)
K = st.number_input(labels[language]["potassium"], 0, 205, 40)

temperature = st.number_input(labels[language]["temperature"], 0.0, 50.0, 25.0)
humidity = st.number_input(labels[language]["humidity"], 0.0, 100.0, 80.0)
ph = st.number_input(labels[language]["ph"], 0.0, 14.0, 6.5)
rainfall = st.number_input(labels[language]["rainfall"], 0.0, 500.0, 200.0)

# ---------------- BUTTON ----------------
if st.button(labels[language]["button"]):

    input_data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=['N','P','K','temperature','humidity','ph','rainfall']
    )

    crop_prediction = model.predict(input_data)[0]
    fert_prediction = fert_model.predict([[temperature, humidity, 40, N, K, P]])[0]

    # 🌍 Translate outputs
    crop_name = translate_text(crop_prediction, lang_codes[language])
    fert_name = translate_text(fert_prediction, lang_codes[language])

    st.success(labels[language]["crop"] + crop_name)
    st.success(labels[language]["fert"] + fert_name)