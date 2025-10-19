import os
import tempfile
import streamlit as st
import openai
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment

# Ensure OpenAI API key is available
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---------------------------
# 🎙️ VOICE INPUT FUNCTIONS
# ---------------------------

def record_voice_input():
    """
    Renders an audio recorder in Streamlit.
    Returns the recorded audio bytes if available.
    """
    st.markdown("### 🎤 Speak your thoughts")
    audio_bytes = st.audio_input("Record your voice message (max 60s)")
    return audio_bytes


def transcribe_audio(audio_bytes):
    """
    Transcribe recorded audio into text using Whisper API.
    Args:
        audio_bytes: raw audio input from Streamlit's audio recorder
    Returns:
        str: Transcribed text
    """
    if not audio_bytes:
        return ""

    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes.read())
        temp_audio_path = temp_audio.name

    try:
        # Whisper transcription
        with open(temp_audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        text = transcript.text.strip()
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        text = ""
    finally:
        os.remove(temp_audio_path)

    return text


# ---------------------------
# 🔊 TEXT TO SPEECH
# ---------------------------

def generate_speech(text):
    """
    Convert AI text response into speech (mp3).
    Args:
        text (str): Text to convert
    Returns:
        BytesIO: Audio stream playable in Streamlit
    """
    if not text:
        return None

    try:
        tts = gTTS(text)
        audio_stream = BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)
        return audio_stream
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None


def play_response_audio(response_text):
    """
    Generate and play speech for a given AI response text.
    """
    st.markdown("### 🔊 AI Voice Response")
    audio_stream = generate_speech(response_text)
    if audio_stream:
        st.audio(audio_stream, format="audio/mp3")


# ---------------------------
# 💡 COMBINED WORKFLOW
# ---------------------------

def handle_voice_interaction(personality="Neutral Therapist"):
    """
    Complete flow:
    1. Record user's voice
    2. Transcribe it to text
    3. Return transcribed text for chat processing
    """
    audio_bytes = record_voice_input()
    if audio_bytes:
        st.info("🎧 Processing your voice input...")
        user_text = transcribe_audio(audio_bytes)
        if user_text:
            st.success(f"🗣️ You said: **{user_text}**")
            return user_text
        else:
            st.warning("Could not understand your voice. Try again!")
    return None
