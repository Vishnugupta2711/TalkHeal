import streamlit as st
import base64
import time
import datetime
import json
from streamlit_lottie import st_lottie

def get_base64_of_bin_file(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background_for_theme(selected_palette="pink"):
    from core.theme import get_current_theme

    # --- Get current theme info ---
    current_theme = st.session_state.get("current_theme", None)
    if not current_theme:
        current_theme = get_current_theme()
    
    is_dark = current_theme["name"] == "Dark"

    # --- Map light themes to background images ---
    palette_color = {
        "light": "static_files/pink.png",
        "calm blue": "static_files/blue.png",
        "mint": "static_files/mint.png",
        "lavender": "static_files/lavender.png",
        "pink": "static_files/pink.png"
    }

    # --- Select background based on theme ---
    if is_dark:
        background_image_path = "static_files/dark.png"
    else:
        background_image_path = palette_color.get(selected_palette.lower(), "static_files/pink.png")

    encoded_string = get_base64_of_bin_file(background_image_path)
    st.markdown(
        f"""
        <style>
        /* Entire app background */
        html, body, [data-testid="stApp"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Main content transparency */
        .block-container {{
            background-color: rgba(255, 255, 255, 0);
        }}

        /* Sidebar: brighter translucent background */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.6);  /* Brighter and translucent */
            color: {'black' if is_dark else 'rgba(49, 51, 63, 0.8)'} ;  /* Adjusted for light background */
        }}
        
        h1 {{
            color: rgb(214, 51, 108) !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}

        h2, h3, h4, h5, h6,
        p, span, strong, div, label {{
            color: {'#f0f0f0' if is_dark else 'rgba(49, 51, 63, 0.8)'} !important;
            transition: color 0.3s ease;
        }}

        /* Header bar: fully transparent */
        [data-testid="stHeader"] {{
            background-color: rgba(0, 0, 0, 0);
        }}

        /* Hide left/right arrow at sidebar bottom */
        button[title="Close sidebar"],
        button[title="Open sidebar"] {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set your background image
selected_palette = st.session_state.get("palette_name", "Pink")
set_background_for_theme(selected_palette)

# --- CONFIG & CONSTANTS ---
TECHNIQUES = {
    "Default Relaxation (4-2-4)": {"inhale": 4, "hold1": 2, "exhale": 4, "hold2": 0},
    "Box Breathing (4-4-4-4)": {"inhale": 4, "hold1": 4, "exhale": 4, "hold2": 4},
    "4-7-8 Breathing": {"inhale": 4, "hold1": 7, "exhale": 8, "hold2": 0},
}
LOTTIE_ANIMATION_PATH = "assets/yoga_animation.json"

# --- STATE MANAGEMENT ---
def initialize_state():
    """Initializes all necessary session state variables."""
    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'SETUP'
    if 'session_log' not in st.session_state:
        st.session_state.session_log = []
    if 'mood_before' not in st.session_state:
        st.session_state.mood_before = 5
    if 'mood_after' not in st.session_state:
        st.session_state.mood_after = None
    if 'session_minutes' not in st.session_state:
        st.session_state.session_minutes = 2
    if 'breathing_technique' not in st.session_state:
        st.session_state.breathing_technique = list(TECHNIQUES.keys())[0]

# --- HELPER FUNCTIONS ---
def load_lottie_animation(filepath):
    """Loads a Lottie animation from a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def calculate_streak(log):
    if not log: return 0
    unique_dates = sorted(list(set([entry['timestamp'].date() for entry in log])), reverse=True)
    today, streak = datetime.date.today(), 0
    if not (unique_dates[0] == today or unique_dates[0] == today - datetime.timedelta(days=1)): return 0
    if unique_dates[0] == today: streak += 1
    for i in range(len(unique_dates) - 1):
        if unique_dates[i] - datetime.timedelta(days=1) == unique_dates[i+1]: streak += 1
        else: break
    if unique_dates[0] == today - datetime.timedelta(days=1) and streak == 0: streak = 1
    return streak

def calculate_weekly_minutes(log):
    one_week_ago = datetime.datetime.now().date() - datetime.timedelta(days=7)
    return sum(entry['duration'] for entry in log if entry['timestamp'].date() > one_week_ago)

# --- UI VIEWS ---
def show_setup_view():
    # --- Inject custom CSS for layout and metrics ---
    st.markdown("""
    <style>
    .breathing-container {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #e6f0ff 0%, #fff 100%);
        border-radius: 18px;
        margin-bottom: 2rem;
    }

    .breathing-container h1 {
        color: #0f766e;
        font-family: 'Baloo 2', cursive;
        font-size: 2.5rem;
        font-weight: 700;
    }

    .breathing-container p {
        color: #333;
        font-size: 1.2rem;
        font-style: italic;
    }

    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    .metric-card h3 {
        margin-bottom: 0.5rem;
        color: #2563eb;
        font-size: 1.1rem;
    }

    .metric-card p {
        margin: 0;
        font-size: 1.3rem;
        font-weight: bold;
        color: #31333F;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Header Section ---
    with st.container():
        st.markdown("""
        <div class="breathing-container">
            <h1>🧘 Breathing Exercise</h1>
            <p>Use this guided exercise to relax. Select a technique, then start your session.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- Progress Section ---
    st.markdown("### 📊 Your Progress")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h3>Current Streak</h3>
                <p>{calculate_streak(st.session_state.session_log)} Days 🔥</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h3>This Week's Total</h3>
                <p>{calculate_weekly_minutes(st.session_state.session_log)} Mins</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- Session Setup Controls ---
    st.markdown("### ⚙️ Session Setup")

    st.session_state.breathing_technique = st.selectbox(
        "Choose a Breathing Technique:", 
        options=list(TECHNIQUES.keys())
    )

    st.session_state.mood_before = st.slider(
        "Rate your current stress level (1 = Low, 10 = High):", 
        1, 10, 5
    )

    st.session_state.session_minutes = st.slider(
        "How many minutes do you want to practice?", 
        1, 15, 2
    )

    if st.button("Start Session"):
        st.session_state.page_state = 'RUNNING'
        st.rerun()

def run_session_view():
    params = TECHNIQUES[st.session_state.breathing_technique]
    inhale, hold1, exhale, hold2 = params['inhale'], params['hold1'], params['exhale'], params['hold2']
    cycle_length = sum(params.values())

    st.markdown(f"<h1 style='text-align: center; color: teal;'>🧘 {st.session_state.breathing_technique}</h1>", unsafe_allow_html=True)
    
    lottie_animation = load_lottie_animation(LOTTIE_ANIMATION_PATH)
    if lottie_animation:
        st_lottie(lottie_animation, height=200, speed=1, quality="high")
    else:
        st.warning("Animation file not found. Displaying a placeholder.")

    timer_placeholder = st.empty()
    breath_text_placeholder = st.empty()
    total_seconds = st.session_state.session_minutes * 60

    for i in range(total_seconds, 0, -1):
        mins, secs = divmod(i, 60)
        timer_placeholder.markdown(f"<h2 style='text-align: center;'>⏳ {mins:02d}:{secs:02d}</h2>", unsafe_allow_html=True)

        phase_time = (total_seconds - i) % cycle_length
        if 0 <= phase_time < inhale: breath_text_placeholder.markdown("<h3 style='text-align: center;'>🌬️ Breathe In...</h3>", unsafe_allow_html=True)
        elif inhale <= phase_time < inhale + hold1: breath_text_placeholder.markdown("<h3 style='text-align: center;'>✋ Hold...</h3>", unsafe_allow_html=True)
        elif inhale + hold1 <= phase_time < inhale + hold1 + exhale: breath_text_placeholder.markdown("<h3 style='text-align: center;'>😮‍💨 Breathe Out...</h3>", unsafe_allow_html=True)
        else: breath_text_placeholder.markdown("<h3 style='text-align: center;'>✋ Hold...</h3>", unsafe_allow_html=True)
        time.sleep(1)

    st.session_state.session_log.append({'timestamp': datetime.datetime.now(), 'duration': st.session_state.session_minutes, 'technique': st.session_state.breathing_technique})
    st.session_state.page_state = 'SUMMARY'
    st.rerun()

def show_summary_view():
    st.balloons()
    st.markdown("<h2 style='text-align: center;'>✅ Session Complete!</h2>", unsafe_allow_html=True)
    st.markdown("--- ")

    st.markdown("### 📈 Your Results")
    st.session_state.mood_after = st.slider("Finally, rate your new stress level (1=Low, 10=High):", 1, 10, st.session_state.mood_before)
    mood_change = st.session_state.mood_after - st.session_state.mood_before
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Starting Stress", f"{st.session_state.mood_before}/10")
    col2.metric("Ending Stress", f"{st.session_state.mood_after}/10")
    col3.metric("Change", f"{mood_change}")

    technique_practiced = st.session_state.session_log[-1]['technique']
    duration_practiced = st.session_state.session_log[-1]['duration']
    st.success(f"Great job! You completed a {duration_practiced}-minute session of {technique_practiced}.")
    st.markdown("--- ")
    if st.button("✨ Start Another Session"):
        st.session_state.page_state = 'SETUP'
        st.session_state.mood_after = None
        st.rerun()

# --- Main App Logic ---
initialize_state()

if st.session_state.page_state == 'SETUP':
    show_setup_view()
elif st.session_state.page_state == 'RUNNING':
    run_session_view()
elif st.session_state.page_state == 'SUMMARY':
    show_summary_view()