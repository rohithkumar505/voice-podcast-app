import streamlit as st
import speech_recognition as sr
import wikipedia
from gtts import gTTS
import os

# Session memory
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak clearly")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Could not understand audio.")
    except sr.RequestError:
        st.error("⚠️ Could not connect to Google.")
    return ""

def get_wikipedia_summary(query):
    try:
        return wikipedia.summary(query, sentences=5)
    except Exception as e:
        st.error(f"❌ Wikipedia Error: {e}")
        return ""

def convert_text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

def main():
    st.set_page_config(page_title="Voice Wikipedia Podcast", page_icon="🎧")

    # Custom Style
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://images.unsplash.com/photo-1523240795612-9a054b0db644");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
        }

        .title-text {
            font-size: 40px;
            color: #FFFF00;
            font-weight: bold;
            text-shadow: 2px 2px 3px black;
        }

        .subtitle-text {
            font-size: 25px;
            color: #00FF00;
            font-weight: bold;
            text-shadow: 2px 2px 3px black;
        }

        .info-text {
            font-size: 18px;
            color: white;
        }

        .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.9);
            color: black;
            font-weight: bold;
        }

        /* 👉 Choose input type label and text input label */
        label[data-baseweb="radio"] {
            font-size: 30px !important;
            color: White !important;
            font-weight: bold;
        }

        .stTextInput label {
            font-size: 28px !important;
            color: #FFFFFF!important;
            font-weight: bold;
        }

        /* 👉 Voice & Text option font */
        div[data-baseweb="radio"] > div {
            font-size: 30px !important;
            color: white !important;
            font-weight: bold;
        }

        audio {
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="title-text">🎧 Voice Wikipedia Podcast Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Ask anything. Listen like a podcast. Speak or type below 👇</div>', unsafe_allow_html=True)

    input_mode = st.radio("CHOOSE INPUT TYPE :", ["🎙️ Voice", "⌨️ Text"])

    if input_mode == "🎙️ Voice":
        if st.button("Start Recording"):
            query = get_voice_input()
            if query:
                st.session_state.last_topic = query
                summary = get_wikipedia_summary(query)
                if summary:
                    st.markdown('<div class="subtitle-text">📖 Wikipedia Summary:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-text">{summary}</div>', unsafe_allow_html=True)
                    audio_file = convert_text_to_speech(summary)
                    st.audio(audio_file, format='audio/mp3')

    else:
        query = st.text_input("Enter your topic:")

        if st.session_state.last_topic:
            st.markdown(f'<div class="info-text">🔁 Last topic: {st.session_state.last_topic}</div>', unsafe_allow_html=True)

        if st.button("Get Story"):
            if query:
                st.session_state.last_topic = query
                summary = get_wikipedia_summary(query)
                if summary:
                    st.markdown('<div class="subtitle-text">📖 Wikipedia Summary:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-text">{summary}</div>', unsafe_allow_html=True)
                    audio_file = convert_text_to_speech(summary)
                    st.audio(audio_file, format='audio/mp3')

if __name__ == "__main__":
    main()





