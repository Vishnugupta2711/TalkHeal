import streamlit as st
import os
from datetime import datetime
import base64

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

        span {{
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

def show():
    # --- Inject custom CSS for consistent layout ---
    st.markdown("""
    <style>
    .main-container {
        padding: 1rem;
    }

    .career-container {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #e6f0ff 0%, #fff 100%);
        border-radius: 18px;
        margin-bottom: 2rem;
    }

    .career-container h1 {
        color: #2563eb;
        font-family: 'Baloo 2', cursive;
        font-size: 2.5rem;
        font-weight: 700;
    }

    .career-container p {
        color: #333;
        font-size: 1.2rem;
        font-style: italic;
    }

    .opening-item {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding: 0.75rem;
        background-color: #f8f9fa;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #31333F;
    }

    .opening-item span {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Careers Header Section ---
    with st.container():
        st.markdown("""
        <div class="career-container">
            <h1>🚀 Careers at TalkHeal</h1>
            <p>Join our mission to support mental wellness and make a real impact!</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- Job Listings ---
    st.subheader("📌 Current Openings")

    openings = {
        "Community Manager": "🤝",
        "Content Writer (Mental Health)": "✍️",
        "Full Stack Developer": "💻",
        "UI/UX Designer": "🎨"
    }

    for role, icon in openings.items():
        st.markdown(f"<div class='opening-item'><span>{icon}</span>{role}</div>", unsafe_allow_html=True)

    st.divider()

    # --- Application Form ---
    st.subheader("📄 Apply Now")

    with st.form("application_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        position = st.selectbox("Position", options=list(openings.keys()))
        resume = st.file_uploader("Upload Your Resume", type=["pdf", "docx"])
        cover_letter = st.text_area("Cover Letter (Optional)")

        submitted = st.form_submit_button("Submit Application")

        if submitted:
            if name and email and position and resume:
                # Save application data
                if not os.path.exists("data/applications"):
                    os.makedirs("data/applications")

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                folder_name = f"{name.replace(' ', '_')}_{timestamp}"
                application_dir = f"data/applications/{folder_name}"
                os.makedirs(application_dir)

                # Save resume
                with open(os.path.join(application_dir, resume.name), "wb") as f:
                    f.write(resume.getbuffer())

                # Save other details
                with open(os.path.join(application_dir, "application.txt"), "w") as f:
                    f.write(f"Name: {name}\n")
                    f.write(f"Email: {email}\n")
                    f.write(f"Position: {position}\n")
                    f.write(f"Cover Letter:\n{cover_letter}")

                st.success("🎉 Your application has been submitted successfully!")
            else:
                st.error("⚠️ Please complete all required fields.")

    st.markdown("</div>", unsafe_allow_html=True) 

    st.info("More roles and opportunities coming soon!")
    
show()