import os
import sys
import types
sys.modules['cgi'] = types.ModuleType('cgi')
import streamlit as st
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
from gtts import gTTS
from googletrans import Translator
import time
import glob
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Traductor por Voz", page_icon="🌎", layout="centered")

# --- TÍTULO Y ENCABEZADO ---
st.markdown(
    """
    <h1 style="text-align:center; color:#1E3A8A;">🌐 Traductor por Voz</h1>
    <p style="text-align:center; color:#2563EB;">Habla, traduce y escucha tu voz en otro idioma</p>
    """,
    unsafe_allow_html=True,
)

# --- IMAGEN DE CABECERA ---
image_url = "https://cdn.pixabay.com/photo/2021/04/02/12/39/translator-6145110_1280.png"
st.image(image_url, width=350)

with st.sidebar:
    st.subheader("🗣️ Cómo usarlo:")
    st.write(
        "1️⃣ Presiona el botón 'Escuchar 🎤'.\n\n"
        "2️⃣ Habla la frase que deseas traducir.\n\n"
        "3️⃣ Selecciona los idiomas y el acento.\n\n"
        "4️⃣ Escucha o descarga el resultado."
    )

st.markdown("### 🎧 Toca el botón y habla lo que quieres traducir")

# --- BOTÓN DE ESCUCHA ---
stt_button = Button(label="🎤 Escuchar", width=300, height=50)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0,
)

# --- PROCESAMIENTO DEL TEXTO ---
if result and "GET_TEXT" in result:
    spoken_text = result.get("GET_TEXT")
    st.success(f"Texto detectado: {spoken_text}")

    os.makedirs("temp", exist_ok=True)

    translator = Translator()

    # --- SELECCIÓN DE IDIOMAS ---
    st.markdown("### 🌍 Configura los idiomas")
    in_lang = st.selectbox(
        "Selecciona el idioma de entrada:",
        ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"),
    )

    out_lang = st.selectbox(
        "Selecciona el idioma de salida:",
        ("Español", "Inglés", "Bengalí", "Coreano", "Mandarín", "Japonés"),
    )

    lang_dict = {
        "Inglés": "en",
        "Español": "es",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja",
    }

    input_language = lang_dict[in_lang]
    output_language = lang_dict[out_lang]

    # --- SELECCIÓN DE ACENTO ---
    st.markdown("### 🎙️ Elige un acento para el audio")
    english_accent = st.selectbox(
        "Acento preferido:",
        ("Defecto", "Español", "Reino Unido", "Estados Unidos", "Canadá", "Australia", "Irlanda", "Sudáfrica"),
    )

    tld_dict = {
        "Defecto": "com",
        "Español": "com.mx",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canadá": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za",
    }

    tld = tld_dict.get(english_accent, "com")

    # --- FUNCIÓN DE TRADUCCIÓN Y VOZ ---
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        filename = "temp/audio.mp3"
        tts.save(filename)
        return filename, trans_text

    display_output_text = st.checkbox("Mostrar texto traducido")

    # --- BOTÓN DE CONVERSIÓN ---
    if st.button("🔊 Convertir y Escuchar"):
        audio_file, translated_text = text_to_speech(input_language, output_language, spoken_text, tld)
        audio_bytes = open(audio_file, "rb").read()

        st.markdown("## 🎧 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3")

        if display_output_text:
            st.markdown("### 📄 Texto traducido:")
            st.info(translated_text)

        # --- DESCARGA ---
        with open(audio_file, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="traduccion.mp3">📥 Descargar audio</a>'
        st.markdown(href, unsafe_allow_html=True)

    # --- LIMPIEZA AUTOMÁTICA ---
    def remove_files(n):
        mp3_files = glob.glob("temp/*.mp3")
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

    remove_files(7)

# --- PIE DE PÁGINA ---
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:#2563EB;">
    Hecho con 🌍 por <b>Santiago Velásquez</b>
    </p>
    """,
    unsafe_allow_html=True,
)
