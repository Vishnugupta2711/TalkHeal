import streamlit as st
import re
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

def newsletter_signup_form():
    """Displays the newsletter signup form and handles submission."""

    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Custom CSS styling
    st.markdown("""
        <style>
        .newsletter-container {
            text-align: center;
            padding: 2rem 1rem;
            background: linear-gradient(135deg, #fceff9 0%, #ffffff 100%);
            border-radius: 18px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }

        .newsletter-container h1 {
            color: #d63384;
            font-family: 'Baloo 2', cursive;
            font-size: 2.5rem;
            font-weight: 700;
        }

        .newsletter-container p {
            color: #333;
            font-size: 1.1rem;
            font-style: italic;
        }

        .newsletter-card {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #eee;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }

        .newsletter-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Container for the header and form
    with st.container():
        st.markdown("""
            <div class="newsletter-container">
                <h1>💌 Subscribe to Our Weekly Newsletter</h1>
                <p>Get the latest wellness tips, mental health news, and exclusive content delivered to your inbox!</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form(key="newsletter_form", clear_on_submit=True):
            email = st.text_input("Email Address", placeholder="Enter your email")
            submit = st.form_submit_button("Subscribe")

            if submit:
                if email and re.match(EMAIL_REGEX, email):
                    st.success("✅ Thank you for subscribing! You'll receive our next newsletter soon.")
                    st.balloons()
                    st.session_state.subscribed = True
                else:
                    st.error("⚠️ Please enter a valid email address.")

        # st.markdown("<p style='text-align: center; color: #888; font-size: 0.9rem;'>We respect your privacy and will never share your email.</p>", unsafe_allow_html=True)
        st.info("🔒 We respect your privacy and will never share your email.")

def show():
    """Renders the Newsletter Signup page."""
    # st.title("📰 Newsletter Signup")

    # Session state check
    if 'subscribed' not in st.session_state:
        st.session_state.subscribed = False

    if st.session_state.subscribed:
        st.success("🎉 You are already subscribed! Thank you for being a part of our community.")
        st.markdown("---")
        st.page_link("app.py", label="Back to Home", icon="🏠")
    else:
        newsletter_signup_form()

    st.divider()
    st.subheader("📖 Past Newsletters")

    past_newsletters = [
        {
            "title": "Mindful Mondays: The Power of Breath",
            "date": "October 6, 2025",
            "summary": "This week, we explore the power of mindful breathing and how it can help you stay calm and centered throughout the day. We also share a simple breathing exercise that you can do anywhere, anytime."
        },
        {
            "title": "Wellness Wednesdays: The Importance of Sleep",
            "date": "September 29, 2025",
            "summary": "In this issue, we dive into the science of sleep and why it's so crucial for your mental and physical health. We also provide some tips for getting a better night's sleep."
        },
        {
            "title": "Feel-Good Fridays: The Benefits of Gratitude",
            "date": "September 22, 2025",
            "summary": "This week, we focus on the power of gratitude and how it can improve your mood and overall well-being. We also share a simple gratitude journaling exercise."
        }
    ]

    cols = st.columns(2)
    for i, newsletter in enumerate(past_newsletters):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="newsletter-card">
                    <h4>{newsletter['title']}</h4>
                    <p><em>{newsletter['date']}</em></p>
                    <p>{newsletter['summary']}</p>
                </div>
            """, unsafe_allow_html=True)

# To run the page
if __name__ == "__main__":
    show()