import streamlit as st
from datetime import datetime
import re
from auth.auth_utils import register_user, authenticate_user , check_user
from auth.mail_utils import send_reset_email
from auth.jwt_utils import create_reset_token
from core.utils import set_authenticated_user
from auth.password_validator import PasswordValidator

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength using NIST guidelines"""
    return PasswordValidator.validate_password(password)

def render_password_strength_meter(password):
    """Render password strength meter with real-time feedback"""
    if not password:
        return

    strength_data = PasswordValidator.calculate_strength(password)
    score = strength_data['score']
    strength = strength_data['strength']
    color = strength_data['color']
    checks = strength_data['checks']
    feedback = strength_data['feedback']

    # Render strength meter
    st.markdown(f"""
    <div class="password-strength-container">
        <div class="strength-meter-wrapper">
            <div class="strength-meter-bar" style="width: {score}%; background-color: {color};"></div>
        </div>
        <div class="strength-label" style="color: {color};">
            {strength} ({score}%)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Render requirements checklist
    st.markdown('<div class="password-requirements">', unsafe_allow_html=True)
    st.markdown('<div class="requirements-title">Password Requirements:</div>', unsafe_allow_html=True)

    requirements = [
        ("✅" if checks['length'] else "❌", "At least 8 characters long", checks['length']),
        ("✅" if checks['uppercase'] else "❌", "Contains uppercase letter (A-Z)", checks['uppercase']),
        ("✅" if checks['lowercase'] else "❌", "Contains lowercase letter (a-z)", checks['lowercase']),
        ("✅" if checks['digit'] else "❌", "Contains number (0-9)", checks['digit']),
        ("✅" if checks['special'] else "❌", "Contains special character (!@#$%^&*)", checks['special']),
        ("✅" if checks['not_common'] else "❌", "Not a common password", checks['not_common']),
        ("✅" if checks['no_sequential'] else "❌", "No sequential characters", checks['no_sequential']),
        ("✅" if checks['no_repeated'] else "❌", "No repeated characters", checks['no_repeated']),
    ]

    for icon, text, passed in requirements:
        color_class = "requirement-met" if passed else "requirement-unmet"
        st.markdown(f'<div class="requirement-item {color_class}">{icon} {text}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Show feedback if not strong enough
    if score < 80 and len(feedback) > 0:
        st.markdown(f'<div class="password-feedback">💡 <strong>Tips:</strong> {", ".join(feedback[:3])}</div>', unsafe_allow_html=True)

def inject_text_visibility_css():
    st.markdown("""
    <style>
    .block-container, .block-container * {
        color: #bf4f70 !important;  /* dark pink */
        font-weight: 600;
        font-size: 16px;}
    </style>
    """, unsafe_allow_html=True)

def show_login_page():
    inject_text_visibility_css()
    """Renders the login/signup page with the modern dark theme."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600&display=swap');
        @keyframes floatHearts {
            0% { transform: translateY(0) scale(1); opacity: 1; }
            100% { transform: translateY(-120px) scale(1.3); opacity: 0; }
        }
        body, html {
            height: 100%;
            min-height: 100vh;
            background: linear-gradient(135deg, #ffe0f0 0%, #ffd6e0 100%);
            font-family: 'Baloo 2', cursive;
        }
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stHeader"] { display: none; }
        .block-container {
            background: linear-gradient(135deg, #fff0f6 60%, #ffe0f0 100%);
            border-radius: 32px;
            max-width: 420px;
            margin: auto;
            margin-top: 60px;
            padding: 2.7rem 3rem 2.2rem 3rem;
            border: 2.5px solid #ffb6d5;
            box-shadow: 0 0 32px 8px #ffd6e0, 0 10px 40px rgba(255, 182, 213, 0.35);
            animation: fadeIn 0.7s ease-out;
            transition: box-shadow 0.2s;
        }
        .block-container:hover {
            box-shadow: 0 0 48px 16px #ffb6d5, 0 10px 40px rgba(255, 182, 213, 0.45);
        }
        .logo-animated {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 0.7rem;
        }
        .logo-animated img {
            width: 74px;
            height: 74px;
            border-radius: 50%;
            box-shadow: 0 0 32px 8px #ffb6d5, 0 2px 16px #ffd6e0;
            background: radial-gradient(circle at 60% 40%, #ffe0f0 70%, #ffb6d5 100%);
            padding: 8px;
            animation: floatLogo 2s infinite alternate ease-in-out;
        }
        @keyframes floatLogo {
            0% { transform: translateY(0); }
            100% { transform: translateY(-12px); }
        }
        .st-emotion-cache-1n6tfoc {
            gap: 0.7rem !important;  
        }
        .auth-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            color: #ff69b4;
            margin-bottom: 0.5rem;
            font-family: 'Baloo 2', cursive;
            letter-spacing: 1px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #ffb6d5;
            margin-bottom: 2.5rem;
            font-family: 'Baloo 2', cursive;
        }
        .auth-input input {
            width: 100%;
            padding: 0.8rem 1rem;
            margin-bottom: 1.25rem;
            border-radius: 12px;
            border: 1.5px solid #ffb6d5;
            background-color: #fff6fa;
            color: #ff69b4;
            font-size: 1rem;
            font-family: 'Baloo 2', cursive;
            transition: all 0.2s ease-in-out;
        }
        .auth-input input::placeholder {
            color: #ffb6d5;
        }
        .auth-input input:focus {
            outline: none;
            border-color: #ff69b4;
            background-color: #ffe0f0;
            box-shadow: 0 0 0 3px rgba(255, 182, 213, 0.3);
        }
        .auth-button {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        .auth-button button {
            width: 100%;
            padding: 0.95rem;
            border-radius: 18px;
            font-weight: 700;
            font-size: 1.18rem;
            border: none;
            color: #fff0f6;
            margin-top: 0.5rem;
            cursor: pointer;
            background: linear-gradient(90deg, #ffb6d5 0%, #ff69b4 100%);
            box-shadow: 0 2px 12px rgba(255, 182, 213, 0.22);
            transition: background 0.2s, box-shadow 0.2s;
            position: relative;
        }
        .auth-button button::after {
            content: " 💖";
            font-size: 1.1rem;
            margin-left: 6px;
        }
        .auth-button button:hover {
            background: linear-gradient(90deg, #ff69b4 0%, #ffb6d5 100%);
            box-shadow: 0 4px 24px rgba(255, 182, 213, 0.32);
        }
        .switch-link {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-top: 1.5rem;
        }
        .switch-link button {
            background: none;
            color: #ff69b4;
            border: none;
            font-size: 1rem;
            text-decoration: none;
            cursor: pointer;
            font-family: 'Baloo 2', cursive;
            transition: color 0.2s;
        }
        .switch-link button:hover {
            color: #ffb6d5;
        }
        /* Password Strength Meter Styles */
        .password-strength-container {
            margin: 1rem 0;
            padding: 0.8rem;
            background: rgba(255, 246, 250, 0.6);
            border-radius: 12px;
            border: 1px solid #ffb6d5;
        }
        .strength-meter-wrapper {
            width: 100%;
            height: 8px;
            background: #ffe0f0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 0.5rem;
        }
        .strength-meter-bar {
            height: 100%;
            transition: width 0.3s ease, background-color 0.3s ease;
            border-radius: 10px;
        }
        .strength-label {
            text-align: center;
            font-size: 0.9rem;
            font-weight: 700;
            font-family: 'Baloo 2', cursive;
            margin-top: 0.3rem;
        }
        .password-requirements {
            margin-top: 1rem;
            padding: 0.8rem;
            background: rgba(255, 246, 250, 0.4);
            border-radius: 10px;
            font-size: 0.85rem;
        }
        .requirements-title {
            font-weight: 700;
            color: #ff69b4;
            margin-bottom: 0.5rem;
            font-family: 'Baloo 2', cursive;
        }
        .requirement-item {
            padding: 0.3rem 0;
            font-family: 'Baloo 2', cursive;
            transition: all 0.2s ease;
        }
        .requirement-met {
            color: #6BCF7F;
        }
        .requirement-unmet {
            color: #FF6B6B;
        }
        .password-feedback {
            margin-top: 0.8rem;
            padding: 0.6rem;
            background: rgba(255, 182, 213, 0.2);
            border-left: 3px solid #ff69b4;
            border-radius: 6px;
            font-size: 0.85rem;
            color: #ff69b4;
            font-family: 'Baloo 2', cursive;
        }
        .password-hint {
            margin: 0.5rem 0;
            padding: 0.5rem;
            text-align: center;
            font-size: 0.9rem;
            color: #ffb6d5;
            font-family: 'Baloo 2', cursive;
            font-style: italic;
        }
        /* Floating hearts animation */
        </style>
        """,
        unsafe_allow_html=True
    )

    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False

    if "show_forget_page" not in st.session_state:
        st.session_state.show_forget_page = False

    if "otp_page" not in st.session_state:
        st.session_state.otp_page = False
    
    
    if "notify_page" not in st.session_state:
        st.session_state.notify_page = False


    is_signup = st.session_state.show_signup
    show_forget_page = st.session_state.show_forget_page
    otp_page = st.session_state.otp_page
    notify_page = st.session_state.notify_page

    if is_signup:
        title = "Create Your Account"
        subtitle_text = "Join TalkHeal to get started 🩷"
    elif notify_page:
        title = "Resent Mail sent"
        subtitle_text = "Please check your inbox."
    elif show_forget_page:
        title = "Reset Your Password"
        subtitle_text = "Enter Your Registered email"
    else:
        title = "Welcome Back Healer!!"
        subtitle_text = "Login to continue your journey 🩷"

    st.markdown('<div class="logo-animated"><img src="https://raw.githubusercontent.com/eccentriccoder01/TalkHeal/main/static_files/TalkHealLogo.png" alt="Logo"/></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="auth-title" style="color:#ffb6d5;">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{subtitle_text}</div>', unsafe_allow_html=True)

    form_container = st.container()

    if is_signup:
        with form_container:
            name = st.text_input("Name", placeholder="Enter your full name", label_visibility="collapsed", key="signup_name")
            email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed", key="signup_email")

            # Password input - Streamlit reruns automatically on every keystroke
            password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed", key="signup_password")

            # Show password strength meter automatically as user types (no need to press Enter)
            if password:
                render_password_strength_meter(password)
            else:
                # Show a hint when password field is empty
                st.markdown('<div class="password-hint">💡 Start typing to see password strength (updates automatically)</div>', unsafe_allow_html=True)

            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("Sign Up", key="signup_submit"):
                if not name or not email or not password:
                    st.error("**Please fill out all fields.**")
                elif not validate_email(email):
                    st.error("**Please enter a valid email address.**")
                else:
                    # Validate password
                    is_valid_password, password_message = validate_password(password)
                    if not is_valid_password:
                        st.error(f"**{password_message}**")
                    else:
                        try:
                            success, message = register_user(name, email, password)
                            if success:
                                st.success("Account created! You can now login.")
                                st.session_state.show_signup = False
                                st.rerun()
                            else:
                                st.error(f"**{message}**")
                        except Exception as e:
                            st.error("**An error occurred during registration. Please try again.**")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="switch-link">', unsafe_allow_html=True)
            if st.button("Already have an account? Login", key="switch_to_login"):
                st.session_state.show_signup = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    elif show_forget_page:
        with form_container:
            email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed", key="signup_email")
            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("Send Reset Link", key="forget_submit"):
                if not email :
                    st.error("**Please fill out email id**")
                elif not validate_email(email):
                    st.error("**Please enter a valid email address.**")
                else:
                    try:
                        success, updated_at = check_user(email)
                        if success:
                            mail_status = send_reset_email(email,create_reset_token(email,updated_at))
                            if mail_status: 
                                st.success("Password Email sent!")
                                st.session_state.show_forget_page = False
                                st.session_state.notify_page=True
                                st.rerun()
                            else:
                                st.error("**Error while Sending Email!**")
                        else:
                            st.error("**User does not exist ! Please Sign Up First**")
                    except Exception as e:
                        st.error("**An error occurred while processing your request. Please try again.**")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="switch-link">', unsafe_allow_html=True)
            if st.button("Already have an account? Login", key="switch_to_login"):
                st.session_state.show_forget_page = False
                # Reset all states to go back to login
                st.session_state.show_signup = False
                st.session_state.notify_page = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    elif notify_page:
        st.success("✅ Password reset email sent! Please check your inbox.")
        st.session_state.notify_page = False  
        st.stop()
    else:
        with form_container:
            email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed", key="login_password")

            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("Login", key="login_submit"):
                if not email or not password:
                    st.error("**Please enter your email and password.**")
                elif not validate_email(email):
                    st.error("**Please enter a valid email address.**")
                else:
                    try:
                        success, user = authenticate_user(email, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user_profile = {
                                "name": user.get("name", ""),
                                "email": user.get("email", email),
                                "profile_picture": user.get("photo", None),
                                "join_date": user.get("join_date", datetime.now().strftime("%B %Y")),
                                "font_size": user.get("font_size", "Medium")
                            }
                            # Set user_name for display purposes
                            st.session_state.user_name = user.get("name", email)
                            st.rerun()
                                            
                        else:
                            st.error("**Invalid email or password.**")
                    except Exception as e:
                        st.error("**An error occurred during login. Please try again.**")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- YOUR NEW CODE STARTS HERE ---
            st.write("--- or ---")

            # Guest Login Button with Full Logic
            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("Login as Guest"):
                # Set the authentication flag to True, just like in a real login
                st.session_state.authenticated = True
                
                # Create a simple, fake user profile for the Guest
                st.session_state.user_profile = {
                    "name": "Guest Healer",
                    "email": "guest@talkheal.app",
                    "profile_picture": None,
                    "join_date": datetime.now().strftime("%B %Y"),
                    "font_size": "Medium"
                }
                # Fix: Use the user_profile instead of undefined 'user' variable
                st.session_state.user_name = st.session_state.user_profile["name"]
                # Rerun the app to enter the main dashboard
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("Forgot Password?", key="switch_to_forget_page"):
                st.session_state.show_signup = False
                st.session_state.show_forget_page = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


            st.markdown('<div class="switch-link">', unsafe_allow_html=True)
            if st.button("Don't have an account? Sign up", key="switch_to_signup"):
                st.session_state.show_signup = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# Main app logic
if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if not st.session_state.authenticated:
        show_login_page()
    else:
        st.title(f"🎉 Welcome, {st.session_state.user_name}!")
        st.success("You're logged in!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_name = ""
            st.rerun()
