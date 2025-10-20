import streamlit as st
import re

def newsletter_signup_form():
    """Displays the newsletter signup form and handles submission."""
    
    # Regex for basic email validation
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    st.markdown("""
        <style>
            .newsletter-container {
                background-color: var(--secondary-background-color);
                color: var(--text-color);
                padding: 2rem;
                border-radius: 10px;
                margin: 2rem auto;
                max-width: 900px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .newsletter-card {
                background-color: var(--background-color);
                border: 1px solid var(--separator-color);
                border-radius: 10px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: box-shadow 0.3s;
            }
            .newsletter-card:hover {
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='newsletter-container'>", unsafe_allow_html=True)
    
    st.header("💌 Subscribe to Our Weekly Newsletter")
    st.write("Get the latest wellness tips, mental health news, and exclusive content delivered straight to your inbox!")
    
    with st.form(key="newsletter_form"):
        email = st.text_input("Email Address", placeholder="Enter your email", key="newsletter_email")
        submit = st.form_submit_button("Subscribe", help="Sign up for our newsletter")
        
        if submit:
            if email and re.match(EMAIL_REGEX, email):
                st.success("Thank you for subscribing! You'll receive our next newsletter soon.")
                st.balloons()
                st.session_state.subscribed = True
            else:
                st.error("Please enter a valid email address.")
    
    st.markdown("<p style='text-align: center; color: #888; font-size: 0.9rem;'>We respect your privacy and will never share your email.</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def show():
    """Renders the Newsletter Signup page."""
    st.title("Newsletter Signup")
    
    # Check if the user has already subscribed in this session
    if 'subscribed' not in st.session_state:
        st.session_state.subscribed = False

    if st.session_state.subscribed:
        st.success("You are already subscribed! Thank you for being a part of our community.")
        st.markdown("---")
        st.page_link("app.py", label="Back to Home", icon="🏠")
    else:
        newsletter_signup_form()

    st.markdown("---")
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