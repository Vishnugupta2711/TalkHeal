import streamlit as st
import time

# Page Config
st.set_page_config(page_title="Feel-Good Zone", page_icon="💖")

# Custom CSS for pink theme
st.markdown(
    """
    <style>
    body {
        background-color: #ffe6f0;
        color: #4a148c;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #f06292;
        color: white;
        border-radius: 12px;
        padding: 0.5em 1em;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #ec407a;
    }
    h1, h2, h3 {
        color: #ad1457;
        text-align: center;
    }
    .exercise-box {
        background-color: #fff0f5;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("💖 Feel-Good Zone")
st.write("Welcome to your safe space! Relax, recharge, and have fun with music, videos, and light exercises.")

# Section: Calming Music
st.header("🎵 Calming Music")
st.write("Unwind with relaxing playlists:")
st.video("https://www.youtube.com/watch?v=2OEL4P1Rz04")

# Section: Motivational Videos
st.header("🎥 Motivational Videos")
st.write("Boost your mood with these inspiring clips:")
st.video("https://www.youtube.com/watch?v=mgmVOuLgFB0")

# Section: Mental Light Exercises
st.header("🧠 Mental Light Exercises")

# Breathing Exercise
with st.container():
    st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
    st.subheader("Breathing Exercise 🌬️")
    if st.button("Start Breathing Exercise"):
        st.write("Inhale... 🫁")
        time.sleep(2)
        st.write("Hold...")
        time.sleep(2)
        st.write("Exhale... 🌬️")
        time.sleep(2)
        st.success("Great job! You are calmer already.")
    st.markdown("</div>", unsafe_allow_html=True)

# Mood Quiz
with st.container():
    st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
    st.subheader("Quick Mood Quiz 🎯")
    mood = st.radio("How are you feeling today?", ["😊 Happy", "😌 Relaxed", "😔 Stressed", "😴 Tired"])
    if st.button("Get Mood Boost"):
        if mood == "😊 Happy":
            st.success("Keep shining bright! 🌟")
        elif mood == "😌 Relaxed":
            st.info("That's wonderful! Maintain this calm energy.")
        elif mood == "😔 Stressed":
            st.warning("Take a deep breath. You’re stronger than you think!")
        elif mood == "😴 Tired":
            st.error("Time for a short break. Maybe some music?")
    st.markdown("</div>", unsafe_allow_html=True)
