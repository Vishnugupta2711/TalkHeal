import streamlit as st
import base64

st.set_page_config(page_title="App Overview", layout="wide")

# --- Asset Loading & Theming ---
def set_page_theme_and_style():
    from core.theme import get_current_theme
    current_theme = st.session_state.get("current_theme") or get_current_theme()
    is_dark = current_theme["name"] == "Dark"
    selected_palette = st.session_state.get("palette_name", "Pink")

    try:
        with open(f"static_files/{'dark.png' if is_dark else selected_palette.lower() + '.png'}", "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        encoded_string = ""

    st.markdown(f'''
        <style>
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        html, body, [data-testid="stApp"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;
        }}
        .block-container {{ background-color: transparent; }}
        [data-testid="stSidebar"] {{ background-color: rgba(255, 255, 255, 0.6); }}
        [data-testid="stHeader"] {{ background-color: transparent; }}
        

        h2 {{ text-align: center; font-weight: 600; margin-bottom: 2rem; }}

        .card {{
            background-color: {'rgba(40, 40, 40, 0.7)' if is_dark else 'rgba(255, 255, 255, 0.7)'};
            border-radius: 15px; padding: 25px; text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: transform 0.2s; height: 100%;
            animation: fadeInUp 0.5s ease-out forwards; opacity: 0;
        }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.2); }}
        .card-icon {{ font-size: 2.5rem; margin-bottom: 10px; }}
        .card-title {{ font-size: 1.15rem; font-weight: 600; margin-bottom: 10px; }}
        
        /* Staggered animation for cards */
        .st-emotion-cache-r421ms:nth-child(1) .card {{ animation-delay: 0.1s; }}
        .st-emotion-cache-r421ms:nth-child(2) .card {{ animation-delay: 0.2s; }}
        .st-emotion-cache-r421ms:nth-child(3) .card {{ animation-delay: 0.3s; }}
        .st-emotion-cache-r421ms:nth-child(4) .card {{ animation-delay: 0.4s; }}
        .st-emotion-cache-r421ms:nth-child(5) .card {{ animation-delay: 0.5s; }}
        </style>
    ''', unsafe_allow_html=True)

# --- Page Layout ---

set_page_theme_and_style()

# --- Header Section ---
st.title("Welcome to TalkHeal")

header_col1, header_col2 = st.columns([1.5, 2])
with header_col1:
    st.image("static_files/Home_Pink.png", use_column_width=True)

with header_col2:
    st.markdown("### Your trusted companion for mental wellness, designed to empower you on your journey to emotional health.")
    st.markdown("TalkHeal provides a safe and supportive space with tools and resources to help you understand your emotions, build healthy habits, and connect with a caring community.")
    st.link_button("💬 Join the Community Forum", "/CommunityForum", use_container_width=True)



# --- Key Features Section ---
st.header("Key Features")

features = [
    {"icon": "📊", "title": "Mood Tracking", "text": "Visualize your emotional patterns and gain insights into your mental state over time."},
    {"icon": "🧘", "title": "Coping Tools", "text": "Engage with guided breathing exercises, journaling, and other self-help utilities."},
    {"icon": "📚", "title": "Resource Hub", "text": "Explore a rich library of articles, guides, and expert advice on various mental health topics."},
    {"icon": "💬", "title": "Community Support", "text": "Connect with peers in a safe, inclusive, and supportive forum environment."},
    {"icon": "🏆", "title": "Personal Dashboard", "text": "Track your progress, view your achievements, and stay motivated on your wellness journey."}
]

feature_cols = st.columns(len(features))
for i, feature in enumerate(features):
    with feature_cols[i]:
        st.markdown(f'''
            <div class="card">
                <div class="card-icon">{feature["icon"]}</div>
                <div class="card-title">{feature["title"]}</div>
                <p>{feature["text"]}</p>
            </div>
        ''', unsafe_allow_html=True)



# --- Why TalkHeal Section ---
st.header("Why TalkHeal?")

why_cols = st.columns(2)
with why_cols[0]:
    st.subheader("User-Centric Design")
    st.markdown("✅ **Soothing & Intuitive:** A calming, user-friendly interface designed to make your wellness journey as smooth as possible.")
    st.markdown("✅ **Cross-Device Access:** Use TalkHeal seamlessly on your phone, tablet, or computer.")
with why_cols[1]:
    st.subheader("Safe & Secure")
    st.markdown("🔒 **Privacy-First:** Your data is kept secure and private, because your trust is our top priority.")
    st.markdown("💰 **Free to Start:** Access core features for free, with affordable options for advanced tools.")

st.markdown("<br><br>", unsafe_allow_html=True)

st.info("**Start your journey with TalkHeal today and discover a happier, healthier you!**", icon="💖")