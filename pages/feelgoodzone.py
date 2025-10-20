import streamlit as st
import time
import random
from datetime import datetime
import json
import os

# Page Config
st.set_page_config(
    page_title="Feel-Good Zone", 
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []
if 'breathing_count' not in st.session_state:
    st.session_state.breathing_count = 0
if 'favorite_quotes' not in st.session_state:
    st.session_state.favorite_quotes = []
if 'gratitude_journal' not in st.session_state:
    st.session_state.gratitude_journal = []

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
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ec407a;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(236, 64, 122, 0.4);
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
    .quote-box {
        background: linear-gradient(135deg, #ffd1dc 0%, #ffb3d9 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        text-align: center;
        font-style: italic;
        font-size: 18px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .gratitude-card {
        background-color: #fff5f8;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #f06292;
    }
    .mood-tracker {
        background: linear-gradient(to right, #ffeef8, #fff0f5);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stProgress > div > div > div > div {
        background-color: #f06292;
    }
    .timer-display {
        font-size: 48px;
        text-align: center;
        color: #ad1457;
        font-weight: bold;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Helper Functions
def save_mood_entry(mood, timestamp):
    """Save mood entry to history."""
    st.session_state.mood_history.append({
        'mood': mood,
        'timestamp': timestamp
    })
    # Keep only last 30 entries
    if len(st.session_state.mood_history) > 30:
        st.session_state.mood_history.pop(0)

def get_mood_emoji(mood):
    """Get emoji for mood."""
    mood_map = {
        "😊 Happy": "😊",
        "😌 Relaxed": "😌",
        "😔 Stressed": "😔",
        "😴 Tired": "😴",
        "🥰 Excited": "🥰",
        "😢 Sad": "😢",
        "😰 Anxious": "😰",
        "😐 Neutral": "😐"
    }
    return mood_map.get(mood, "😊")

def get_random_affirmation():
    """Get a random positive affirmation."""
    affirmations = [
        "You are stronger than you think! 💪",
        "Every day is a fresh start. 🌅",
        "You deserve all the good things coming your way. ✨",
        "Your feelings are valid and important. 💖",
        "You are doing better than you realize. 🌟",
        "It's okay to take things one step at a time. 🚶",
        "You are worthy of love and respect. 💕",
        "Your journey is unique and beautiful. 🦋",
        "You have the power to create positive change. 🌈",
        "You are enough, just as you are. 🌸"
    ]
    return random.choice(affirmations)

def get_random_inspirational_quote():
    """Get a random inspirational quote."""
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Be yourself; everyone else is already taken. - Oscar Wilde",
        "In the middle of difficulty lies opportunity. - Albert Einstein",
        "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
        "Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "It does not matter how slowly you go as long as you do not stop. - Confucius",
        "Everything you've ever wanted is on the other side of fear. - George Addair",
        "Start where you are. Use what you have. Do what you can. - Arthur Ashe"
    ]
    return random.choice(quotes)

def get_activity_suggestion(mood):
    """Get activity suggestion based on mood."""
    suggestions = {
        "😊 Happy": "Keep the positive vibes! Try journaling about what made you happy today. 📝",
        "😌 Relaxed": "Perfect time for meditation or a gentle walk in nature. 🌳",
        "😔 Stressed": "Take deep breaths, listen to calming music, or talk to someone you trust. 🫂",
        "😴 Tired": "Rest is important! Take a power nap or do some gentle stretching. 😴",
        "🥰 Excited": "Channel that energy into something creative or fun! 🎨",
        "😢 Sad": "It's okay to feel sad. Be gentle with yourself and do something comforting. 🤗",
        "😰 Anxious": "Try the 5-4-3-2-1 grounding technique or progressive muscle relaxation. 🧘",
        "😐 Neutral": "A great time to explore something new or revisit a favorite hobby. 🎯"
    }
    return suggestions.get(mood, "Take care of yourself! 💖")

def save_to_file(data, filename):
    """Save data to JSON file."""
    try:
        os.makedirs('data', exist_ok=True)
        with open(f'data/{filename}', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.warning(f"Could not save data: {e}")

def load_from_file(filename):
    """Load data from JSON file."""
    try:
        if os.path.exists(f'data/{filename}'):
            with open(f'data/{filename}', 'r') as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load data: {e}")
    return []

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/hearts.png", width=80)
    st.title("💖 Your Wellness Hub")
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📊 Your Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Breathing Sessions", st.session_state.breathing_count)
    with col2:
        st.metric("Mood Checks", len(st.session_state.mood_history))
    
    st.markdown("---")
    
    # Daily Affirmation
    st.subheader("✨ Daily Affirmation")
    if st.button("🔄 New Affirmation"):
        st.session_state.current_affirmation = get_random_affirmation()
    
    if 'current_affirmation' not in st.session_state:
        st.session_state.current_affirmation = get_random_affirmation()
    
    st.info(st.session_state.current_affirmation)
    
    st.markdown("---")
    
    # Quick Access
    st.subheader("⚡ Quick Access")
    page = st.radio(
        "Navigate to:",
        ["🏠 Home", "🎵 Music & Videos", "🧠 Exercises", "📔 Journal", "📊 Mood Tracker"],
        label_visibility="collapsed"
    )

# Main Content
if page == "🏠 Home":
    # Title
    st.title("💖 Feel-Good Zone")
    st.write("Welcome to your safe space! Relax, recharge, and have fun with music, videos, and light exercises.")
    
    # Random Inspirational Quote
    st.markdown("<div class='quote-box'>", unsafe_allow_html=True)
    if st.button("✨ Get Inspired"):
        st.session_state.daily_quote = get_random_inspirational_quote()
    
    if 'daily_quote' not in st.session_state:
        st.session_state.daily_quote = get_random_inspirational_quote()
    
    st.markdown(f"*{st.session_state.daily_quote}*")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Mood Check
    st.subheader("💭 How are you feeling right now?")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("😊 Happy", use_container_width=True):
            save_mood_entry("😊 Happy", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.balloons()
            st.success("Wonderful! Keep spreading that joy! 🌟")
    
    with col2:
        if st.button("😌 Relaxed", use_container_width=True):
            save_mood_entry("😌 Relaxed", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.success("That's great! Enjoy this peaceful moment. 🕊️")
    
    with col3:
        if st.button("😔 Stressed", use_container_width=True):
            save_mood_entry("😔 Stressed", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.info("Take a deep breath. You've got this! 💪")
    
    with col4:
        if st.button("😴 Tired", use_container_width=True):
            save_mood_entry("😴 Tired", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.info("Rest is productive too. Be kind to yourself. 🛌")
    
    st.markdown("---")
    
    # Featured Activities
    st.subheader("🌟 Featured Activities Today")
    
    activity_col1, activity_col2, activity_col3 = st.columns(3)
    
    with activity_col1:
        with st.container():
            st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
            st.markdown("### 🎵 Calming Sounds")
            st.write("5-minute relaxation session")
            if st.button("Start Now 🎧", key="quick_music"):
                st.switch_page("pages/music_videos.py") if "music_videos.py" else st.info("Play your favorite calming music!")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with activity_col2:
        with st.container():
            st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
            st.markdown("### 🌬️ Breathing Exercise")
            st.write("Quick 2-minute session")
            if st.button("Breathe 🫁", key="quick_breathing"):
                st.info("Redirecting to breathing exercises...")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with activity_col3:
        with st.container():
            st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
            st.markdown("### 📝 Gratitude Journal")
            st.write("Write what you're grateful for")
            if st.button("Start Writing ✍️", key="quick_journal"):
                st.info("Opening journal...")
            st.markdown("</div>", unsafe_allow_html=True)

elif page == "🎵 Music & Videos":
    st.title("🎵 Music & Videos")
    
    # Section: Calming Music
    st.header("🎵 Calming Music")
    st.write("Unwind with relaxing playlists:")
    
    music_tab1, music_tab2, music_tab3, music_tab4, music_tab5 = st.tabs([
        "🌊 Nature Sounds", "🎹 Instrumental", "🧘 Meditation", "☕ Coffee Shop", "🌙 Sleep Music"
    ])
    
    with music_tab1:
        st.subheader("Ocean Waves & Nature")
        st.video("https://www.youtube.com/watch?v=2OEL4P1Rz04")
        st.write("**Benefits:** Reduces stress, improves focus, promotes relaxation")
        st.markdown("---")
        
        st.subheader("Rain Sounds for Sleeping")
        st.video("https://www.youtube.com/watch?v=q76bMs-NwRk")
        st.write("**Perfect for:** Deep sleep, meditation, relaxation")
        st.markdown("---")
        
        st.subheader("Forest Sounds - Birds Singing")
        st.video("https://www.youtube.com/watch?v=xNN7iTA57jM")
        st.write("**Great for:** Morning meditation, stress relief, nature connection")
    
    with music_tab2:
        st.subheader("Peaceful Piano Music")
        st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")
        st.write("**Perfect for:** Study sessions, work, creative activities")
        st.markdown("---")
        
        st.subheader("Beautiful Relaxing Music")
        st.video("https://www.youtube.com/watch?v=lTRiuFIWV54")
        st.write("**Ideal for:** Stress relief, meditation, peaceful background")
        st.markdown("---")
        
        st.subheader("Calming Guitar Music")
        st.video("https://www.youtube.com/watch?v=TUzYcO4етро")
        st.write("**Best for:** Relaxation, evening wind-down, contemplation")
    
    with music_tab3:
        st.subheader("Tibetan Meditation Music")
        st.video("https://www.youtube.com/watch?v=inpok4MKVLM")
        st.write("**Great for:** Deep relaxation, sleep preparation, mindfulness")
        st.markdown("---")
        
        st.subheader("Healing Sleep Music")
        st.video("https://www.youtube.com/watch?v=t0kJn-U36hE")
        st.write("**Benefits:** Deep sleep, stress relief, body healing")
        st.markdown("---")
        
        st.subheader("Chakra Meditation Music")
        st.video("https://www.youtube.com/watch?v=ARaZwj67p6Q")
        st.write("**Purpose:** Energy balance, spiritual healing, inner peace")
    
    with music_tab4:
        st.subheader("Coffee Shop Ambience")
        st.video("https://www.youtube.com/watch?v=gaGlB26EdMg")
        st.write("**Perfect for:** Working, studying, feeling cozy")
        st.markdown("---")
        
        st.subheader("Jazz Music for Work")
        st.video("https://www.youtube.com/watch?v=fEvM-OUbaKs")
        st.write("**Ideal for:** Concentration, productivity, creative flow")
        st.markdown("---")
        
        st.subheader("Cozy Coffee Shop Vibes")
        st.video("https://www.youtube.com/watch?v=kgx4WGK0oNU")
        st.write("**Great for:** Reading, relaxing, background ambience")
    
    with music_tab5:
        st.subheader("Deep Sleep Music")
        st.video("https://www.youtube.com/watch?v=1ZYbU82GVz4")
        st.write("**Benefits:** Fall asleep faster, stay asleep longer, wake refreshed")
        st.markdown("---")
        
        st.subheader("Sleeping Music for Insomnia")
        st.video("https://www.youtube.com/watch?v=nDq6TstdEi8")
        st.write("**Helps with:** Insomnia, anxiety, racing thoughts")
        st.markdown("---")
        
        st.subheader("Relaxing Sleep Music with Nature")
        st.video("https://www.youtube.com/watch?v=eKFTSSKCzWA")
        st.write("**Perfect for:** Bedtime routine, stress relief, peaceful sleep")
    
    st.markdown("---")
    
    # Section: Motivational Videos
    st.header("🎥 Motivational Videos")
    st.write("Boost your mood with these inspiring clips:")
    
    video_tab1, video_tab2, video_tab3, video_tab4, video_tab5 = st.tabs([
        "💪 Motivation", "🌟 Inspiration", "😊 Feel-Good", "🎯 Success Stories", "💖 Self-Love"
    ])
    
    with video_tab1:
        st.subheader("Best Motivational Speech")
        st.video("https://www.youtube.com/watch?v=mgmVOuLgFB0")
        st.write("**Message:** Never give up on your dreams!")
        st.markdown("---")
        
        st.subheader("I WILL NOT QUIT - Motivational Video")
        st.video("https://www.youtube.com/watch?v=OFkJgHwymm8")
        st.write("**Theme:** Persistence, determination, overcoming obstacles")
        st.markdown("---")
        
        st.subheader("BELIEVE IN YOURSELF")
        st.video("https://www.youtube.com/watch?v=tYzMYcUty6s")
        st.write("**Message:** Self-belief is the foundation of success")
    
    with video_tab2:
        st.subheader("Life is Beautiful")
        st.video("https://www.youtube.com/watch?v=Lp7E973zozc")
        st.write("**Takeaway:** Small steps lead to big changes")
        st.markdown("---")
        
        st.subheader("The Power of Gratitude")
        st.video("https://www.youtube.com/watch?v=JMd1CcGZYwU")
        st.write("**Message:** Appreciate what you have, attract more positivity")
        st.markdown("---")
        
        st.subheader("Your Life is Your Story")
        st.video("https://www.youtube.com/watch?v=KlUMrzwmbyo")
        st.write("**Theme:** Take control of your narrative, write your own story")
    
    with video_tab3:
        st.subheader("Happy & Uplifting Music")
        st.video("https://www.youtube.com/watch?v=d-diB65scQU")
        st.write("**Theme:** Spreading positivity and joy")
        st.markdown("---")
        
        st.subheader("Funny Animal Videos")
        st.video("https://www.youtube.com/watch?v=hY7m5jjJ9mM")
        st.write("**Purpose:** Instant mood boost, laughter therapy")
        st.markdown("---")
        
        st.subheader("Random Acts of Kindness")
        st.video("https://www.youtube.com/watch?v=nwAYpLVyeFU")
        st.write("**Message:** Kindness creates ripples of positivity")
    
    with video_tab4:
        st.subheader("From Nothing to Something")
        st.video("https://www.youtube.com/watch?v=HCgKRaZwmEA")
        st.write("**Story:** Real people overcoming incredible odds")
        st.markdown("---")
        
        st.subheader("Failure to Success Stories")
        st.video("https://www.youtube.com/watch?v=45mMioJ5szc")
        st.write("**Lesson:** Failure is a stepping stone to success")
        st.markdown("---")
        
        st.subheader("Never Too Late to Start")
        st.video("https://www.youtube.com/watch?v=q8LaT5Iiwo4")
        st.write("**Message:** Age is just a number, pursue your dreams now")
    
    with video_tab5:
        st.subheader("You Are Enough")
        st.video("https://www.youtube.com/watch?v=kQjtK32mGJQ")
        st.write("**Message:** Self-acceptance and self-love are essential")
        st.markdown("---")
        
        st.subheader("Self-Care is Not Selfish")
        st.video("https://www.youtube.com/watch?v=w6T02g5hnT4")
        st.write("**Theme:** Prioritize your mental health and well-being")
        st.markdown("---")
        
        st.subheader("Positive Affirmations")
        st.video("https://www.youtube.com/watch?v=5fLLu03xLbk")
        st.write("**Purpose:** Reprogram your mind with positive thoughts")
    
    # Custom Playlist
    st.markdown("---")
    st.subheader("🎶 Create Your Playlist")
    
    playlist_name = st.text_input("Playlist Name", placeholder="My Feel-Good Mix")
    playlist_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Add to My Playlist"):
        if playlist_name and playlist_url:
            st.success(f"Added '{playlist_name}' to your playlist! 🎵")
        else:
            st.warning("Please fill in both fields!")

elif page == "🧠 Exercises":
    st.title("🧠 Mental Light Exercises")
    
    # Breathing Exercise
    with st.container():
        st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
        st.subheader("Breathing Exercise 🌬️")
        st.write("Follow the guided breathing pattern to calm your mind.")
        
        breathing_col1, breathing_col2 = st.columns([2, 1])
        
        with breathing_col1:
            breathing_type = st.selectbox(
                "Choose breathing technique:",
                ["4-7-8 Breathing", "Box Breathing", "Simple Deep Breathing"]
            )
            
            if st.button("Start Breathing Exercise", key="main_breathing"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                if breathing_type == "4-7-8 Breathing":
                    # 4-7-8 technique
                    for cycle in range(3):
                        status_text.markdown("### 🫁 Inhale through nose (4 seconds)")
                        for i in range(4):
                            progress_bar.progress((i + 1) * 25)
                            time.sleep(1)
                        
                        status_text.markdown("### ⏸️ Hold (7 seconds)")
                        for i in range(7):
                            progress_bar.progress(min(100, (i + 1) * 14))
                            time.sleep(1)
                        
                        status_text.markdown("### 🌬️ Exhale through mouth (8 seconds)")
                        for i in range(8):
                            progress_bar.progress(100 - (i + 1) * 12)
                            time.sleep(1)
                        
                        progress_bar.progress(0)
                
                elif breathing_type == "Box Breathing":
                    # Box breathing (4-4-4-4)
                    for cycle in range(3):
                        status_text.markdown("### 🫁 Inhale (4 seconds)")
                        for i in range(4):
                            progress_bar.progress((i + 1) * 25)
                            time.sleep(1)
                        
                        status_text.markdown("### ⏸️ Hold (4 seconds)")
                        for i in range(4):
                            time.sleep(1)
                        
                        status_text.markdown("### 🌬️ Exhale (4 seconds)")
                        for i in range(4):
                            progress_bar.progress(100 - (i + 1) * 25)
                            time.sleep(1)
                        
                        status_text.markdown("### ⏸️ Hold (4 seconds)")
                        for i in range(4):
                            time.sleep(1)
                        
                        progress_bar.progress(0)
                
                else:
                    # Simple deep breathing
                    for cycle in range(5):
                        status_text.markdown("### 🫁 Inhale deeply... (3 seconds)")
                        for i in range(3):
                            progress_bar.progress((i + 1) * 33)
                            time.sleep(1)
                        
                        status_text.markdown("### 🌬️ Exhale slowly... (3 seconds)")
                        for i in range(3):
                            progress_bar.progress(100 - (i + 1) * 33)
                            time.sleep(1)
                        
                        progress_bar.progress(0)
                
                status_text.markdown("### ✅ Great job! You are calmer already.")
                st.balloons()
                st.session_state.breathing_count += 1
        
        with breathing_col2:
            st.info(f"**Sessions Today:** {st.session_state.breathing_count}")
            st.write("**Benefits:**")
            st.write("• Reduces anxiety")
            st.write("• Lowers heart rate")
            st.write("• Improves focus")
            st.write("• Promotes relaxation")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Progressive Muscle Relaxation
    with st.container():
        st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
        st.subheader("Progressive Muscle Relaxation 💆")
        st.write("Tense and release different muscle groups to reduce physical tension.")
        
        if st.button("Start PMR Session"):
            muscle_groups = [
                ("Hands and Arms", "Make tight fists, then release"),
                ("Face and Jaw", "Scrunch your face, then relax"),
                ("Shoulders and Neck", "Raise shoulders to ears, then drop"),
                ("Chest and Back", "Take deep breath and tighten, then release"),
                ("Legs and Feet", "Point toes and tighten legs, then relax")
            ]
            
            progress = st.progress(0)
            status = st.empty()
            
            for idx, (group, instruction) in enumerate(muscle_groups):
                status.markdown(f"### {group}")
                st.write(f"**{instruction}**")
                st.write("Tense for 5 seconds...")
                time.sleep(5)
                st.write("Now release and feel the relaxation...")
                time.sleep(5)
                progress.progress((idx + 1) * 20)
            
            st.success("✨ Complete! Notice how relaxed your body feels now.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Grounding Exercise (5-4-3-2-1)
    with st.container():
        st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
        st.subheader("Grounding Exercise (5-4-3-2-1) 🌍")
        st.write("Use your senses to ground yourself in the present moment.")
        
        if st.button("Start Grounding Exercise"):
            st.markdown("### Take a deep breath and look around you...")
            time.sleep(2)
            
            st.markdown("**👀 Name 5 things you can SEE**")
            for i in range(5):
                st.text_input(f"Thing {i+1} you see:", key=f"see_{i}")
            
            st.markdown("**✋ Name 4 things you can TOUCH**")
            for i in range(4):
                st.text_input(f"Thing {i+1} you can touch:", key=f"touch_{i}")
            
            st.markdown("**👂 Name 3 things you can HEAR**")
            for i in range(3):
                st.text_input(f"Sound {i+1} you hear:", key=f"hear_{i}")
            
            st.markdown("**👃 Name 2 things you can SMELL**")
            for i in range(2):
                st.text_input(f"Smell {i+1}:", key=f"smell_{i}")
            
            st.markdown("**👅 Name 1 thing you can TASTE**")
            st.text_input("Taste:", key="taste")
            
            if st.button("Complete Exercise"):
                st.success("🎉 Well done! You're more present and grounded now.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mood Quiz
    with st.container():
        st.markdown("<div class='exercise-box'>", unsafe_allow_html=True)
        st.subheader("Quick Mood Quiz 🎯")
        
        mood = st.radio(
            "How are you feeling today?",
            ["😊 Happy", "😌 Relaxed", "😔 Stressed", "😴 Tired", "🥰 Excited", "😢 Sad", "😰 Anxious", "😐 Neutral"]
        )
        
        if st.button("Get Mood Boost"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_mood_entry(mood, timestamp)
            
            if mood == "😊 Happy":
                st.success("Keep shining bright! 🌟")
            elif mood == "😌 Relaxed":
                st.info("That's wonderful! Maintain this calm energy.")
            elif mood == "😔 Stressed":
                st.warning("Take a deep breath. You're stronger than you think!")
            elif mood == "😴 Tired":
                st.error("Time for a short break. Maybe some music?")
            elif mood == "🥰 Excited":
                st.success("Love that energy! Channel it into something fun!")
            elif mood == "😢 Sad":
                st.info("It's okay to feel sad. Be gentle with yourself. 💙")
            elif mood == "😰 Anxious":
                st.warning("Try some breathing exercises. You've got this! 🫂")
            elif mood == "😐 Neutral":
                st.info("A perfect time to explore something new! 🌈")
            
            # Show activity suggestion
            st.markdown("---")
            st.markdown(f"**💡 Suggestion:** {get_activity_suggestion(mood)}")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "📔 Journal":
    st.title("📔 Gratitude & Reflection Journal")
    st.write("Writing down your thoughts and gratitudes can improve mental well-being.")
    
    journal_tab1, journal_tab2 = st.tabs(["✍️ New Entry", "📖 Past Entries"])
    
    with journal_tab1:
        st.subheader("What are you grateful for today?")
        
        gratitude_1 = st.text_input("Gratitude 1:", placeholder="I'm grateful for...")
        gratitude_2 = st.text_input("Gratitude 2:", placeholder="I'm grateful for...")
        gratitude_3 = st.text_input("Gratitude 3:", placeholder="I'm grateful for...")
        
        st.subheader("How was your day?")
        journal_entry = st.text_area(
            "Write your thoughts:",
            placeholder="Today I felt...\nSomething good that happened was...\nI'm proud of myself for...",
            height=200
        )
        
        if st.button("💾 Save Entry", type="primary"):
            if gratitude_1 or gratitude_2 or gratitude_3 or journal_entry:
                entry = {
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'gratitudes': [g for g in [gratitude_1, gratitude_2, gratitude_3] if g],
                    'journal': journal_entry
                }
                st.session_state.gratitude_journal.append(entry)
                save_to_file(st.session_state.gratitude_journal, 'journal.json')
                st.success("✅ Journal entry saved! Great job reflecting today. 🌟")
                st.balloons()
            else:
                st.warning("Please write something before saving!")
    
    with journal_tab2:
        if not st.session_state.gratitude_journal:
            st.info("No entries yet. Start writing to see your journal here!")
        else:
            st.write(f"**Total Entries:** {len(st.session_state.gratitude_journal)}")
            
            for idx, entry in enumerate(reversed(st.session_state.gratitude_journal)):
                with st.container():
                    st.markdown("<div class='gratitude-card'>", unsafe_allow_html=True)
                    st.markdown(f"### 📅 {entry['date']} - {entry['time']}")
                    
                    if entry.get('gratitudes'):
                        st.markdown("**🙏 Gratitudes:**")
                        for g in entry['gratitudes']:
                            st.markdown(f"• {g}")
                    
                    if entry.get('journal'):
                        st.markdown("**📝 Journal:**")
                        st.write(entry['journal'])
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("---")

elif page == "📊 Mood Tracker":
    st.title("📊 Mood Tracker")
    st.write("Track your emotional well-being over time.")
    
    if not st.session_state.mood_history:
        st.info("No mood data yet. Check in with your feelings to start tracking!")
    else:
        # Statistics
        st.subheader("📈 Your Mood Statistics")
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.metric("Total Check-ins", len(st.session_state.mood_history))
        
        with stat_col2:
            moods = [entry['mood'] for entry in st.session_state.mood_history]
            most_common = max(set(moods), key=moods.count) if moods else "N/A"
            st.metric("Most Common Mood", get_mood_emoji(most_common))
        
        with stat_col3:
            today_moods = [
                entry for entry in st.session_state.mood_history
                if entry['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d"))
            ]
            st.metric("Check-ins Today", len(today_moods))
        
        st.markdown("---")
        
        # Recent Moods
        st.subheader("🕐 Recent Mood Check-ins")
        
        for entry in reversed(st.session_state.mood_history[-10:]):
            with st.container():
                st.markdown("<div class='mood-tracker'>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 2])
                with col1:
                    st.markdown(f"## {get_mood_emoji(entry['mood'])}")
                with col2:
                    st.write(f"**{entry['mood'].replace('😊', '').replace('😌', '').replace('😔', '').replace('😴', '').replace('🥰', '').replace('😢', '').replace('😰', '').replace('😐', '').strip()}**")
                with col3:
                    st.write(entry['timestamp'])
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export Data
        if st.button("📥 Export Mood Data"):
            mood_data = "Timestamp,Mood\n"
            mood_data += "\n".join([f"{entry['timestamp']},{entry['mood']}" for entry in st.session_state.mood_history])
            st.download_button(
                label="Download CSV",
                data=mood_data,
                file_name=f"mood_tracker_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #ad1457; padding: 20px;">
    <p><strong>Remember:</strong> It's okay to not be okay. You're doing great! 💖</p>
    <p style="font-size: 0.9rem;">Take care of yourself, one moment at a time. 🌸</p>
</div>
""", unsafe_allow_html=True)

