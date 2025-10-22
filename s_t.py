import streamlit as st
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
from st_audiorec import st_audiorec
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Traductor por voz", page_icon="🎧", layout="centered")

st.markdown("""
    <style>
    body, .stApp { background-color: #0f1c2e; color: white; }
    h1, h2, h3 { color: #58a6ff; text-align: center; }
    .stButton button {
        background-color: #1e3a5f !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid #58a6ff;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #58a6ff !important;
        color: #0f1c2e !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎤 Traductor por voz")
st.subheader("Escucha, traduce y reproduce tu voz — por Santiago Velasquez")

image_url = "https://cdn.pixabay.com/photo/2020/05/28/02/53/headphones-5222602_1280.jpg"
st.image(image_url, use_column_width=True)

with st.sidebar:
    st.header("🌍 Ajustes del traductor")
    st.write("Graba tu voz desde el navegador, elige idiomas y traduce fácilmente.")

# Grabar audio
st.markdown("### 🎧 Graba tu voz:")
audio_bytes = st_audiorec()

text = None
if audio_bytes:
    st.success("✅ Audio grabado correctamente.")
    recognizer = sr.Recognizer()
    with sr.AudioFile(BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
            st.write("🗣 Texto detectado:", text)
        except Exception as e:
            st.error("No se pudo reconocer el audio. Intenta hablar más claro o más corto.")
            text = None

if text:
    translator = Translator()

    col1, col2 = st.columns(2)
    with col1:
        input_lang = st.selectbox("Idioma de entrada", ["Español", "Inglés", "Francés", "Japonés", "Coreano"])
    with col2:
        output_lang = st.selectbox("Idioma de salida", ["Inglés", "Español", "Francés", "Japonés", "Coreano"])

    lang_codes = {
        "Español": "es",
        "Inglés": "en",
        "Francés": "fr",
        "Japonés": "ja",
        "Coreano": "ko"
    }

    input_code = lang_codes[input_lang]
    output_code = lang_codes[output_lang]

    translation = translator.translate(text, src=input_code, dest=output_code)
    translated_text = translation.text

    st.markdown("### 🌐 Traducción:")
    st.write(translated_text)

    if st.button("🔊 Reproducir traducción"):
        tts = gTTS(translated_text, lang=output_code)
        tts.save("translation.mp3")
        st.audio("translation.mp3", format="audio/mp3")

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>Desarrollado por <b>Santiago Velasquez</b></p>", unsafe_allow_html=True)
