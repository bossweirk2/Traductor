import os
import streamlit as st
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from gtts import gTTS
from googletrans import Translator
import random, time, glob

# ------------------ CONFIGURACIÓN GENERAL ------------------
st.set_page_config(page_title="Traductor Poético Futurista", page_icon="🪶", layout="centered")

# ---- ESTILOS FUTURISTAS ----
st.markdown("""
    <style>
    body {
        background-color: #0b0f19;
        color: #e0e0e0;
    }
    .main {
        background: radial-gradient(circle at 20% 20%, #141a2e, #0b0f19 70%);
        border: 1px solid #222;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 0 25px #00f7ff20;
    }
    h1, h2, h3 {
        color: #8af3ff;
        text-shadow: 0 0 8px #00f7ff80;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d0ff, #7f00ff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.5em;
        font-size: 16px;
        transition: 0.3s;
        font-weight: 600;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #00f7ff80;
    }
    .neon {
        color: #a7f7ff;
        text-shadow: 0 0 8px #00f7ff, 0 0 12px #8a2be280;
        font-style: italic;
    }
    .poem-box {
        background-color: #141a2e;
        border: 1px solid #00f7ff30;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 0 12px #00f7ff20;
        font-size: 1.1rem;
        line-height: 1.5;
        color: #e3f6ff;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ INTERFAZ ------------------
st.title("🪶 Traductor Poético Futurista")
st.caption("Convierte tu voz en versos interestelares 🌌")

translator = Translator()

# ------------------ CAPTURA DE VOZ ------------------
st.subheader("🎙️ Habla tu inspiración")

stt_button = Button(label="🎧 Escuchar tu voz", width=300)
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
)

if result and "GET_TEXT" in result:
    text = result.get("GET_TEXT")
    st.success("✨ Texto capturado:")
    st.markdown(f"<div class='neon'>“{text}”</div>", unsafe_allow_html=True)
else:
    text = ""

# ------------------ FUNCIONES ------------------

def crear_poema(texto_base):
    """Genera un poema simple basado en el texto de entrada."""
    lineas = [
        f"Entre las sombras del código, {texto_base.lower()},",
        f"un susurro viaja entre líneas de luz,",
        f"la máquina escucha, siente, traduce,",
        f"y convierte tu voz en un sueño azul.",
        f"Tu frase cruza fronteras del alma,",
        f"se vuelve eco en la red estelar,",
        f"donde los bytes respiran calma,",
        f"y las palabras aprenden a amar.",
    ]
    random.shuffle(lineas)
    return "\n".join(lineas)

def text_to_speech(text):
    """Convierte texto a audio con gTTS"""
    tts = gTTS(text, lang="es", tld="com", slow=False)
    os.makedirs("temp", exist_ok=True)
    path = "temp/poema.mp3"
    tts.save(path)
    return path

def remove_old_files():
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < time.time() - 86400:
            os.remove(f)

remove_old_files()

# ------------------ GENERACIÓN POÉTICA ------------------
if st.button("💫 Generar poema"):
    if text:
        poema = crear_poema(text)
        st.markdown("<div class='poem-box'>" + poema.replace("\n", "<br>") + "</div>", unsafe_allow_html=True)
        st.audio(text_to_speech(poema), format="audio/mp3")
    else:
        st.warning("Por favor, habla algo antes de generar el poema.")

# ------------------ MODO EXTRA: TRADUCCIÓN ------------------
st.markdown("---")
st.subheader("🌐 Traducir el poema (opcional)")

idioma_destino = st.selectbox("Selecciona el idioma de destino", ["Inglés", "Francés", "Japonés", "Coreano"])
mapa_idiomas = {"Inglés": "en", "Francés": "fr", "Japonés": "ja", "Coreano": "ko"}

if st.button("🌍 Traducir poema"):
    if text:
        poema = crear_poema(text)
        traduccion = translator.translate(poema, dest=mapa_idiomas[idioma_destino]).text
        st.markdown(f"#### ✨ Poema en {idioma_destino}:")
        st.markdown(f"<div class='poem-box'>{traduccion}</div>", unsafe_allow_html=True)
    else:
        st.warning("Primero genera o graba tu poema.")

# ------------------ FOOTER ------------------
st.markdown("""
---
<div style='text-align:center; color:#777; font-size:0.9rem'>
Hecho con 💙 por un algoritmo que sueña en binario.<br>
<em>“Donde la voz humana se transforma en poesía digital.”</em>
</div>
""", unsafe_allow_html=True)
