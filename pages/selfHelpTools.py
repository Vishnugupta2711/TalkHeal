import streamlit as st
import webbrowser
from datetime import datetime
from core.utils import create_new_conversation, get_current_time
from core.theme import get_current_theme, toggle_theme, set_palette, PALETTES
from components.mood_dashboard import render_mood_dashboard, MoodTracker
from components.profile import initialize_profile_state, render_profile_section
from components.focus_session import render_focus_session
from components.quick_coping_cards import render_quick_coping_cards
from components.thought_reframing import render_thought_reframing
from components.sleep_hygiene import render_sleep_hygiene_toolkit
from components.medication_reminder import render_medication_reminder
from components.self_compassion import render_self_compassion_tool
from components.crisis_action_plan import render_crisis_action_plan
from components.pomodoro_focus import render_pomodoro_focus
from components.pmr_guide import render_pmr_guide
from components.values_clarification import render_values_clarification
from components.therapy_tool import render_therapy_tool
from components.playlist_generator import render_playlist_generator
from streamlit_js_eval import streamlit_js_eval
import requests
import base64
import json

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css = """
    <style>
    /* Entire app background */
    html, body, [data-testid="stApp"] {
        background-image: url("data:image/png;base64,{BASE64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Main content transparency */
    .block-container {
        background-color: rgba(255, 255, 255, 0);
    }

    /* Sidebar: brighter translucent background */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.6);
        color: black;
    }

    /* Header bar: fully transparent */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }

    /* Hide left/right arrow at sidebar bottom */
    button[title="Close sidebar"],
    button[title="Open sidebar"] {
        display: none !important;
    }

    /* 🌟 Custom link styling */
    a {
        color: #ffffff !important;   /* White links */
        font-weight: 500;
        text-decoration: none;
    }
    a:hover {
        color: #FFD700 !important;   /* Gold hover */
        text-decoration: underline;
    }
    </style>
    """

    st.markdown(css.replace("{BASE64}", encoded_string), unsafe_allow_html=True)


# ✅ Set your background image
set_background("static_files/lavender.png")


# --- Structured Emergency Resources ---
GLOBAL_RESOURCES = [
    {"name": "Befrienders Worldwide", "desc": "Emotional support to prevent suicide worldwide.",
        "url": "https://www.befrienders.org/"},
    {"name": "International Association for Suicide Prevention (IASP)", "desc": "Find a crisis center anywhere in the world.",
     "url": "https://www.iasp.info/resources/Crisis_Centres/"},
    {"name": "Crisis Text Line", "desc": "Text-based support available in the US, UK, Canada, and Ireland.",
     "url": "https://www.crisistextline.org/"},
    {"name": "The Trevor Project", "desc": "Crisis intervention and suicide prevention for LGBTQ young people.",
     "url": "https://www.thetrevorproject.org/"},
    {"name": "Child Helpline International", "desc": "A global network of child helplines for young people in need of help.",
     "url": "https://www.childhelplineinternational.org/"}
]


def get_country_from_coords(lat, lon):
    try:
        url = f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("address", {}).get("country_code", "").upper()
    except:
        pass
    return None

def get_user_country():
    # 1. Try to get user's actual browser location (via JS)
    coords = streamlit_js_eval(
        js_expressions="""
            new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(
                    position => resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    }),
                    error => resolve(null)
                );
            });
        """,
        key="get_coords"
    )

    if coords and "latitude" in coords and "longitude" in coords:
        country = get_country_from_coords(coords["latitude"], coords["longitude"])
        if country:
            return country

    # 2. Fallback to IP-based location using ipapi.co (no key required)
    try:
        resp = requests.get("https://ipapi.co/json/", timeout=3)
        if resp.status_code == 200:
            return resp.json().get("country_code", "").upper()
    except:
        pass

    return None  # final fallback if everything fails

with open("data/country_helplines.json", "r") as f:
    country_helplines = json.load(f)

country_names = {
    "US": "United States",
    "IN": "India",
    "GB": "United Kingdom",
    "AU": "Australia",
    "CA": "Canada",
    "DE": "Germany",
    "FR": "France",
    "NZ": "New Zealand",
    "ZA": "South Africa"
}
IASP_LINK = "https://findahelpline.com/"

# Enhanced Knowledge Base with icons
mental_health_resources_full = {
    "Depression & Mood Disorders": {
        "icon": "😔",
        "description": "Information on understanding and coping with depression, persistent depressive disorder, and other mood-related challenges.",
        "links": [
            {"label": "NIMH - Depression", "url": "https://www.nimh.nih.gov/health/topics/depression"},
            {"label": "Mayo Clinic - Depression", "url": "https://www.mayoclinic.org/diseases-conditions/depression/symptoms-causes/syc-20356007"}
        ],
        "tags": ["Depression", "Mood Disorders", "Mental Health", "Coping Skills"]
    },
    "Anxiety & Panic Disorders": {
        "icon": "😨",
        "description": "Guidance on managing generalized anxiety, social anxiety, panic attacks, and phobias.",
        "links": [
            {"label": "ADAA - Anxiety & Depression", "url": "https://adaa.org/"},
            {"label": "NIMH - Anxiety Disorders", "url": "https://www.nimh.nih.gov/health/topics/anxiety-disorders"}
        ],
        "tags": ["Anxiety", "Panic Attacks", "Phobias", "Stress Management", "Mental Health"]
    },
    "Bipolar Disorder": {
        "icon": "🎭",
        "description": "Understanding the complexities of bipolar disorder, including mood swings and treatment options.",
        "links": [
            {"label": "NIMH - Bipolar Disorder", "url": "https://www.nimh.nih.gov/health/topics/bipolar-disorder"}
        ],
        "tags": ["Bipolar", "Mood Disorders", "Mental Health", "Treatment Options"]
    },
    "PTSD & Trauma": {
        "icon": "🧠",
        "description": "Resources for individuals experiencing post-traumatic stress disorder and other trauma-related conditions.",
        "links": [
            {"label": "PTSD: National Center", "url": "https://www.ptsd.va.gov/"}
        ],
        "tags": ["PTSD", "Trauma", "Mental Health", "Coping Skills"]
    },
    "OCD & Related Disorders": {
        "icon": "🔄",
        "description": "Support and information for obsessive-compulsive disorder, body dysmorphic disorder, and hoarding disorder.",
        "links": [
            {"label": "IOCDF - OCD", "url": "https://iocdf.org/"}
        ],
        "tags": ["OCD", "Mental Health", "Coping Skills"]
    },
    "Coping Skills & Self-Care": {
        "icon": "❤️‍🩹",
        "description": "Practical strategies and techniques for stress management, emotional regulation, and daily well-being.",
        "links": [
            {"label": "HelpGuide - Stress Management", "url": "https://www.helpguide.org/articles/stress/stress-management.htm"}
        ],
        "tags": ["Coping Skills", "Self-Care", "Stress Management", "Emotional Regulation", "Well-being", "Mindfulness"]
    },
    "Therapy & Treatment Options": {
        "icon": "🗣️",
        "description": "Overview of various therapeutic approaches, including CBT, DBT, and finding a therapist.",
        "links": [
            {"label": "APA - Finding a Therapist", "url": "https://www.apa.org/helpcenter/choose-therapist"}
        ],
        "tags": ["Therapy", "Treatment Options", "CBT", "DBT", "Mental Health Professionals"]
    }
}
st.title("🧰 Self Help Tools")

tools = {
    "focus": {"name": "Focus Session", "icon": "🧘"},
    "pomodoro": {"name": "Pomodoro Focus", "icon": "⏱️"},
    "pmr": {"name": "Muscle Relaxation (PMR)", "icon": "🧩"},
    "values": {"name": "Values Clarification", "icon": "🎯"},
    "therapy": {"name": "Therapy Prep & Notes", "icon": "📈"},
    "playlist": {"name": "Playlist Generator", "icon": "🎵"},
    "mood_dashboard": {"name": "Mood Dashboard", "icon": "📊"},
    "mental_check": {"name": "Mental Health Check", "icon": "🧠"},
    "thought_reframing": {"name": "Thought Reframing (CBT)", "icon": "💭"},
    "sleep_hygiene": {"name": "Sleep Hygiene Toolkit", "icon": "🌙"},
    "medication_reminder": {"name": "Medication Reminder", "icon": "🔔"},
    "self_compassion": {"name": "Self-Compassion Practice", "icon": "🌱"},
    "crisis_plan": {"name": "Crisis Action Plan", "icon": "🆘"},
    "knowledge": {"name": "Knowledge Base", "icon": "📚"},
    "crisis": {"name": "Crisis Support", "icon": "☎️"},
    "quizzes": {"name": "PsyToolkit Quizzes", "icon": "🧪"},
    "quick_coping": {"name": "Quick Coping Cards", "icon": "🃏"},
    "grounding_exercise": {"name": "Grounding Exercise", "icon": "🌳"},
}

# --- Initialize session state for favorites and recents ---
if "active_tool" not in st.session_state:
    st.session_state.active_tool = ""

if "recent_tools" not in st.session_state:
    st.session_state.recent_tools = []


if "favorite_tools" not in st.session_state:
    st.session_state.favorite_tools = []

# --- Display Favorite Tools ---
if st.session_state.favorite_tools:
    st.subheader("⭐ Favorites")
    # Limit to 4 columns for favorites
    fav_cols = st.columns(min(len(st.session_state.favorite_tools), 4))
    for i, tool_id in enumerate(st.session_state.favorite_tools):
        with fav_cols[i % 4]:
            if st.button(f"{tools[tool_id]['icon']} {tools[tool_id]['name']}", key=f"fav_{tool_id}", use_container_width=True):
                st.session_state.active_tool = tool_id

                # Add to recents when a favorite is clicked
                if tool_id not in st.session_state.recent_tools:
                    st.session_state.recent_tools.insert(0, tool_id)
                    # Keep recents list to a max of 4
                    if len(st.session_state.recent_tools) > 4:
                        st.session_state.recent_tools.pop()
                st.rerun()

# --- Display Recent Tools ---
if st.session_state.recent_tools:
    st.subheader("🕓 Recents")
    # Limit to 4 columns for recents
    rec_cols = st.columns(min(len(st.session_state.recent_tools), 4))
    for i, tool_id in enumerate(st.session_state.recent_tools):
        with rec_cols[i % 4]:
            if st.button(f"{tools[tool_id]['icon']} {tools[tool_id]['name']}", key=f"rec_{tool_id}", use_container_width=True):
                st.session_state.active_tool = tool_id
                st.rerun()

# --- Display All Tools with Favorite Toggles ---
st.subheader("All Tools")
# Use 2 columns for the main tool list
cols = st.columns(2)
for i, (tool_id, tool_info) in enumerate(tools.items()):
    with cols[i % 2]:
        # Create a layout with the main button and a smaller favorite button
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(f"{tool_info['icon']} {tool_info['name']}", use_container_width=True, key=f"tool_{tool_id}"):
                st.session_state.active_tool = tool_id
                # Add to recents when a tool is clicked
                if tool_id not in st.session_state.recent_tools:
                    st.session_state.recent_tools.insert(0, tool_id)
                    # Keep recents list to a max of 4
                    if len(st.session_state.recent_tools) > 4:
                        st.session_state.recent_tools.pop()
                st.rerun()

        with col2:
            # Check if the tool is already a favorite
            is_favorited = tool_id in st.session_state.favorite_tools
            # Use a star icon to indicate favorite status
            if st.button("⭐" if is_favorited else "☆", key=f"fav_toggle_{tool_id}", use_container_width=True):
                if is_favorited:
                    st.session_state.favorite_tools.remove(tool_id)
                else:
                    st.session_state.favorite_tools.append(tool_id)
                st.rerun()

st.markdown("---")

# --- RENDER SELECTED TOOL ---
if st.session_state.active_tool == "focus":
    st.header("🧘 Focus Session")
    render_focus_session()

elif st.session_state.active_tool == "pomodoro":
    render_pomodoro_focus()

elif st.session_state.active_tool == "pmr":
    render_pmr_guide()

elif st.session_state.active_tool == "values":
    render_values_clarification()

elif st.session_state.active_tool == "therapy":
    render_therapy_tool()

elif st.session_state.active_tool == "playlist":
    render_playlist_generator()

elif st.session_state.active_tool == "mood_dashboard":
    render_mood_dashboard()

elif st.session_state.active_tool == "mental_check":
    st.header("🧠 Mental Health Check")
    mood_options_map = {
        "😔 Very Low": "very_low",
        "😐 Low": "low",
        "😊 Okay": "okay",
        "😄 Good": "good",
        "🌟 Great": "great"
    }
    mood_labels = list(mood_options_map.keys())
    selected_mood_label = st.radio("Mood Scale", options=mood_labels, index=mood_labels.index("😊 Okay"), horizontal=True)
    st.session_state.current_mood_val = mood_options_map[selected_mood_label]

    journal_prompt_text = {
        "very_low": "What's weighing on your mind today?",
        "low": "What are your thoughts right now?",
        "okay": "Anything specific on your mind today?",
        "good": "What made you feel good today?",
        "great": "What's making you shine today?"
    }.get(st.session_state.current_mood_val, "Reflect on your mood:")

    if "mood_journal_entry" not in st.session_state:
        st.session_state.mood_journal_entry = ""
    if "mood_tip_display" not in st.session_state:
        st.session_state.mood_tip_display = ""
    if "mood_entry_status" not in st.session_state:
        st.session_state.mood_entry_status = ""

    st.text_area(f"✏️ {journal_prompt_text}", key="mood_journal_area", value=st.session_state.mood_journal_entry, height=70)

    st.markdown("**Why are you feeling this way?**")
    if "custom_reasons" not in st.session_state:
        st.session_state.custom_reasons = []
    
    default_reasons = ["No specific reason", "Work", "Family", "Health", "Relationships", "Financial", "Social", "Personal goals", "Weather", "Other"]
    all_reasons = default_reasons + st.session_state.custom_reasons
    
    selected_reason = st.selectbox("Select a reason (optional):", options=all_reasons, key="mood_reason_select")
    
    new_custom_reason = st.text_input("Add a custom reason (optional):", key="new_custom_reason_input")
    if st.button("Add Custom Reason", key="add_custom_reason_button") and new_custom_reason.strip():
        if new_custom_reason.strip() not in st.session_state.custom_reasons:
            st.session_state.custom_reasons.append(new_custom_reason.strip())
            st.session_state.new_custom_reason_input = "" # Clear input after adding
            st.rerun()

    st.markdown("**What did you do today?** (optional)")
    if "custom_activities" not in st.session_state:
        st.session_state.custom_activities = []
    if "selected_activities" not in st.session_state:
        st.session_state.selected_activities = []

    default_activities = ["Exercise", "Socialized", "Ate healthy", "Slept well", "Meditated", "Worked", "Relaxed", "Hobbies"]
    all_activities_options = sorted(list(set(default_activities + st.session_state.custom_activities)))

    # Display checkboxes for all activities
    cols_per_row = 2
    num_cols = st.columns(cols_per_row)
    for i, activity in enumerate(all_activities_options):
        with num_cols[i % cols_per_row]:
            # Use a unique key for each checkbox
            if st.checkbox(f"✅ {activity}", key=f"activity_checkbox_{activity}", value=activity in st.session_state.selected_activities):
                if activity not in st.session_state.selected_activities:
                    st.session_state.selected_activities.append(activity)
            else:
                if activity in st.session_state.selected_activities:
                    st.session_state.selected_activities.remove(activity)

    new_custom_activity = st.text_input("Add a custom activity (optional):", key="new_custom_activity_input")
    if st.button("Add Custom Activity", key="add_custom_activity_button") and new_custom_activity.strip():
        if new_custom_activity.strip() not in st.session_state.custom_activities:
            st.session_state.custom_activities.append(new_custom_activity.strip())
            st.session_state.new_custom_activity_input = "" # Clear input after adding
            st.rerun()
    
    # Update the activities list to be saved
    activities = st.session_state.selected_activities

    tips_for_mood = {
        "very_low": "Remember, it's okay not to be okay. Consider connecting with a professional.",
        "low": "Even small steps help. Try a brief mindful moment or gentle activity.",
        "okay": "Keep nurturing your well-being. What's one thing you can do to maintain this?",
        "good": "That's wonderful! Savor this feeling and perhaps share your positivity.",
        "great": "Fantastic! How can you carry this energy forward into your day?"
    }.get(st.session_state.current_mood_val, "A general tip for your mood.")

    col_tip, col_talk = st.columns(2)
    with col_tip:
        if st.button("Get Tip & Save Entry"):
            if "mood_tracker" not in st.session_state:
                st.session_state.mood_tracker = MoodTracker()
            st.session_state.mood_tracker.add_mood_entry(
                st.session_state.current_mood_val,
                st.session_state.get("mood_journal_area", ""),
                selected_reason,
                activities
            )
            st.session_state.mood_tip_display = tips_for_mood
            st.session_state.mood_entry_status = f"Mood entry for '{selected_mood_label}' saved."
            st.session_state.mood_journal_entry = ""

    with col_talk:
        if st.button("Ask TalkHeal"):
            if st.session_state.mood_journal_area.strip():
                st.session_state.pre_filled_chat_input = st.session_state.mood_journal_area
                st.session_state.send_chat_message = True
                st.session_state.mood_journal_entry = ""
                st.session_state.mood_tip_display = ""
                st.session_state.mood_entry_status = ""
                st.rerun()
            else:
                st.warning("Please enter your thoughts before asking TalkHeal.")

    if st.session_state.mood_tip_display:
        st.success(st.session_state.mood_tip_display)
    if st.session_state.mood_entry_status:
        st.info(st.session_state.mood_entry_status)

elif st.session_state.active_tool == "thought_reframing":
    render_thought_reframing()

elif st.session_state.active_tool == "sleep_hygiene":
    render_sleep_hygiene_toolkit()

elif st.session_state.active_tool == "medication_reminder":
    render_medication_reminder()

elif st.session_state.active_tool == "self_compassion":
    render_self_compassion_tool()

elif st.session_state.active_tool == "crisis_plan":
    render_crisis_action_plan()

elif st.session_state.active_tool == "knowledge":
    st.header("📚 Resources & Knowledge Base")

    if "link_to_share" not in st.session_state:
        st.session_state.link_to_share = None

    all_tags = sorted(list(set(tag for data in mental_health_resources_full.values() for tag in data.get("tags", []))))
    selected_tags = st.multiselect("Filter by Tags:", options=all_tags, placeholder="Select tags to filter resources")

    query = st.text_input("Search resources by topic...", placeholder="e.g., anxiety, ptsd, self-care")

    # Filter topics based on search query and selected tags
    filtered_topics = {}
    for topic, data in mental_health_resources_full.items():
        matches_query = True
        if query:
            matches_query = query.lower() in topic.lower() or query.lower() in data['description'].lower()

        matches_tags = True
        if selected_tags:
            matches_tags = any(tag in data.get("tags", []) for tag in selected_tags)

        if matches_query and matches_tags:
            filtered_topics[topic] = data

    if not filtered_topics:
        st.info(f"No resources found matching your criteria. Please try another search term or different tags.")
    else:
        # Use st.expander for a cleaner, more scalable layout
        for topic, data in filtered_topics.items():
            with st.expander(f"{data['icon']} {topic}", expanded=bool(query) or bool(selected_tags)):
                st.info(data['description'])

                st.markdown("Tags: " + ", ".join([f"`{tag}`" for tag in data.get("tags", [])]))

                for link in data['links']:
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.markdown(f"**[{link['label']}]({link['url']})**")
                        # Extract domain for context
                        domain = link['url'].split('/')[2]
                        st.caption(f"🔗 {domain}")
                    with col2:
                        if st.button("Share", key=f"share_{link['url']}"):
                            st.session_state.link_to_share = link['url']

    if st.session_state.link_to_share:
        st.text_input("Copy this link:", value=st.session_state.link_to_share, key="share_input")
        if st.button("Close", key="close_share"):
            st.session_state.link_to_share = None

elif st.session_state.active_tool == "crisis":
    st.header("☎️ Crisis Support")
    
    search_query = st.text_input("Search for a specific resource or helpline:", "")
    
    st.subheader("Global Resources")
    
    filtered_global_resources = [
        r for r in GLOBAL_RESOURCES
        if search_query.lower() in r['name'].lower() or search_query.lower() in r['desc'].lower()
    ]
    
    if not filtered_global_resources:
        st.info("No global resources found matching your search.")
    else:
        for r in filtered_global_resources:
            st.markdown(f"**{r['name']}**: {r['desc']} [Visit Website]({r['url']})")
    
    st.info("""
    **What to expect when you call a helpline:**
    You'll connect with a trained crisis counselor who can provide confidential support.
    You don't need to be suicidal to call; they can help with various emotional distress.
    They are there to listen without judgment and help you explore options.
    """)

    user_country_auto = get_user_country()
    st.markdown("### 🚨 Emergency Help")

    # Allow user to manually select country
    all_available_countries = sorted(list(country_helplines.keys()))
    default_country_index = 0
    if user_country_auto and user_country_auto in all_available_countries:
        default_country_index = all_available_countries.index(user_country_auto)

    selected_country = st.selectbox(
        "Select your country for local helplines:",
        options=all_available_countries,
        index=default_country_index,
        format_func=lambda x: f"{x} - {country_names.get(x, 'Unknown')}"
    )

    if selected_country and selected_country in country_helplines:
        st.markdown(f"**Helplines for {selected_country} ({country_names.get(selected_country, 'Unknown')}):**")
        
        filtered_helplines = [
            line for line in country_helplines[selected_country]
            if search_query.lower() in line.lower()
        ]
        
        if not filtered_helplines:
            st.info(f"No helplines found matching your search for {selected_country}.")
        else:
            for line in filtered_helplines:
                st.markdown(f"• {line}")
    else:
        st.markdown(f"[Find help worldwide via IASP]({IASP_LINK})")

elif st.session_state.active_tool == "quizzes":
    st.header("🧪 Take PsyToolkit Verified Quizzes")
    quizzes = [
        {
            "name": "GAD-7 (Anxiety Assessment)",
            "desc": "Measures severity of generalized anxiety symptoms.",
            "url": "https://www.psytoolkit.org/cgi-bin/3.6.0/survey?s=u8bAf",
            "score": "0–4: Minimal, 5–9: Mild, 10–14: Moderate, 15–21: Severe"
        },
        {
            "name": "PHQ-9 (Depression Assessment)",
            "desc": "Screens for presence and severity of depression.",
            "url": "https://www.psytoolkit.org/cgi-bin/3.6.0/survey?s=Hj32b",
            "score": "0–4: Mild, 5–9: Moderate, 10–14: Moderately Severe, 15–19: Severe"
        },
        {
            "name": "WHO-5 Well-Being Index",
            "desc": "Five simple questions to assess well-being. 0 (poor) to 100 (excellent).",
            "url": "https://www.psytoolkit.org/cgi-bin/3.6.0/survey?s=POqLJ",
            "score": "Score <= 50 may indicate need for further assessment."
        },
        {
            "name": "DASS (Depression, Anxiety, Stress Scale)",
            "desc": "Measures all three using one combined form.",
            "url": "https://www.psytoolkit.org/cgi-bin/3.6.0/survey?s=HvfDY",
            "score": "Normal to Extremely Severe per subscale"
        }
    ]
    for q in quizzes:
        st.markdown(f"**{q['name']}**\n\n*{q['desc']}*\n\n[Take Quiz]({q['url']})\n\nScore Info: {q['score']}")
        st.markdown("---")

elif st.session_state.active_tool == "quick_coping":
    render_quick_coping_cards()

elif st.session_state.active_tool == "grounding_exercise":
    st.header("🌳 5-4-3-2-1 Grounding Exercise")

    if "grounding_step" not in st.session_state:
        st.session_state.grounding_step = 0
    if "grounding_responses" not in st.session_state:
        st.session_state.grounding_responses = {
            "see": [], "feel": [], "hear": [], "smell": [], "taste": []
        }
    if "selected_audio" not in st.session_state:
        st.session_state.selected_audio = "None"

    audio_files = ["None", "forest_ambience.wav", "gentle_piano.wav", "ocean_waves.wav", "rain_sounds.wav", "silent_soft_music.wav", "tibetan_bowls.wav"]
    st.session_state.selected_audio = st.selectbox("Select background audio:", options=audio_files, index=audio_files.index(st.session_state.selected_audio))

    if st.session_state.selected_audio != "None":
        try:
            st.audio(f"audio_files/{st.session_state.selected_audio}")
        except FileNotFoundError:
            st.warning(f"Audio file {st.session_state.selected_audio} not found.")

    steps = [
        {"prompt": "5 things you can SEE", "key": "see", "count": 5, "icon": "👀"},
        {"prompt": "4 things you can FEEL", "key": "feel", "count": 4, "icon": "🖐️"},
        {"prompt": "3 things you can HEAR", "key": "hear", "count": 3, "icon": "👂"},
        {"prompt": "2 things you can SMELL", "key": "smell", "count": 2, "icon": "👃"},
        {"prompt": "1 thing you can TASTE", "key": "taste", "count": 1, "icon": "👅"}
    ]
    
    step_icons = {step['key']: step['icon'] for step in steps}

    progress = st.session_state.grounding_step / len(steps)
    st.progress(progress)

    if st.session_state.grounding_step < len(steps):
        current_step_info = steps[st.session_state.grounding_step]
        st.subheader(f"Step {st.session_state.grounding_step + 1}: {current_step_info['icon']} {current_step_info['prompt']}")
        
        responses = []
        for i in range(current_step_info["count"]):
            response = st.text_input(f"Item {i+1}", key=f"grounding_input_{current_step_info['key']}_{i}")
            responses.append(response)

        col_next, col_reset = st.columns([1, 1])
        with col_next:
            if st.button("Next Step", use_container_width=True):
                # Filter out empty responses
                filled_responses = [r.strip() for r in responses if r.strip()]
                if len(filled_responses) < current_step_info['count']:
                    st.warning(f"Please list at least {current_step_info['count']} items.")
                else:
                    st.session_state.grounding_responses[current_step_info['key']] = filled_responses
                    st.session_state.grounding_step += 1
                    st.rerun()
        with col_reset:
            if st.button("Start Over", use_container_width=True):
                st.session_state.grounding_step = 0
                st.session_state.grounding_responses = {
                    "see": [], "feel": [], "hear": [], "smell": [], "taste": []
                }
                st.rerun()
    else:
        st.subheader("🎉 Grounding Exercise Complete!")
        st.success("You've completed the 5-4-3-2-1 grounding exercise. Take a deep breath.")

        st.markdown("### Your Responses:")
        for key, value in st.session_state.grounding_responses.items():
            st.markdown(f"**{step_icons[key]} {key.capitalize()}:**")
            for item in value:
                st.write(f"- {item}")
        
        if st.button("Start New Exercise", use_container_width=True):
            st.session_state.grounding_step = 0
            st.session_state.grounding_responses = {
                "see": [], "feel": [], "hear": [], "smell": [], "taste": []
            }
            st.rerun()