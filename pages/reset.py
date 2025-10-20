import streamlit as st
import base64
from components.reset_page import show_reset_password_page
from datetime import datetime, timedelta

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
        
        /* Enhanced reset page styles */
        .reset-container {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            padding: 3rem;
            margin: 2rem auto;
            max-width: 600px;
            backdrop-filter: blur(10px);
        }}
        
        .error-container {{
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left: 5px solid #dc2626;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.15);
        }}
        
        .info-container {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 5px solid #3b82f6;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        }}
        
        .success-container {{
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border-left: 5px solid #10b981;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
        }}
        
        .warning-container {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 5px solid #f59e0b;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
        }}
        
        .help-box {{
            background: rgba(255, 255, 255, 0.7);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }}
        
        .link-button {{
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #d14a7a 0%, #c13d6e 100%);
            color: white !important;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(209, 74, 122, 0.3);
            margin: 0.5rem;
        }}
        
        .link-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(209, 74, 122, 0.4);
        }}
        
        .security-note {{
            background: rgba(147, 51, 234, 0.1);
            border: 1px solid rgba(147, 51, 234, 0.3);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            font-size: 0.9rem;
        }}
        
        .countdown-timer {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #d14a7a;
            text-align: center;
            padding: 1rem;
            background: rgba(209, 74, 122, 0.1);
            border-radius: 8px;
            margin: 1rem 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set your background image
selected_palette = st.session_state.get("palette_name", "Pink")
set_background_for_theme(selected_palette)

# --- Grab token from URL ---
reset_token = st.query_params.get("token")

# --- Initialize session state ---
if "reset_token" not in st.session_state:
    st.session_state.reset_token = None
if "show_reset_page" not in st.session_state:
    st.session_state.show_reset_page = False
if "token_checked" not in st.session_state:
    st.session_state.token_checked = False
if "token_valid" not in st.session_state:
    st.session_state.token_valid = None
if "token_expiry" not in st.session_state:
    st.session_state.token_expiry = None
if "reset_attempts" not in st.session_state:
    st.session_state.reset_attempts = 0
if "last_reset_time" not in st.session_state:
    st.session_state.last_reset_time = None

# --- If token exists in URL, save it and show reset page ---
if reset_token:
    st.session_state.reset_token = reset_token
    st.session_state.show_reset_page = True

def validate_token(token):
    """
    Validate the reset token.
    This is a placeholder - implement your actual token validation logic.
    """
    # TODO: Implement actual token validation against your database
    # Check if token exists, not expired, not already used
    
    # Example validation (replace with your actual logic)
    if not token or len(token) < 20:
        return False, "Invalid token format"
    
    # Check token expiry (example: tokens expire after 1 hour)
    # In production, check against database timestamp
    # For now, we'll assume token is valid
    
    return True, None

def show_error_page(error_type="invalid"):
    """Display appropriate error page based on error type"""
    
    st.markdown("<div class='reset-container'>", unsafe_allow_html=True)
    
    if error_type == "invalid":
        st.markdown("""
            <div class='error-container'>
                <h2 style='color: #dc2626; margin-top: 0;'>
                    ❌ Invalid Reset Link
                </h2>
                <p style='color: #333; font-size: 1.1rem;'>
                    The password reset link you're trying to use is invalid or malformed.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    elif error_type == "expired":
        st.markdown("""
            <div class='error-container'>
                <h2 style='color: #dc2626; margin-top: 0;'>
                    ⏰ Link Expired
                </h2>
                <p style='color: #333; font-size: 1.1rem;'>
                    This password reset link has expired. For security reasons, reset links are only valid for 1 hour.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    elif error_type == "used":
        st.markdown("""
            <div class='error-container'>
                <h2 style='color: #dc2626; margin-top: 0;'>
                    🔒 Link Already Used
                </h2>
                <p style='color: #333; font-size: 1.1rem;'>
                    This password reset link has already been used. Each link can only be used once for security.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    elif error_type == "no_token":
        st.markdown("""
            <div class='info-container'>
                <h2 style='color: #3b82f6; margin-top: 0;'>
                    📧 Password Reset Required
                </h2>
                <p style='color: #333; font-size: 1.1rem;'>
                    No reset token was provided. Please use the password reset link from your email.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Common help section for all error types
    st.markdown("""
        <div class='help-box'>
            <h3 style='color: #d14a7a; margin-top: 0;'>
                💡 What to do next?
            </h3>
            <ul style='color: #333; line-height: 1.8;'>
                <li><strong>Request a new reset link:</strong> Go to the login page and click "Forgot Password"</li>
                <li><strong>Check your email:</strong> Make sure you're using the most recent reset email</li>
                <li><strong>Copy the full link:</strong> Ensure you copied the entire URL from the email</li>
                <li><strong>Try again:</strong> Reset links are valid for 1 hour from the time they're sent</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔑 Request New Link", use_container_width=True):
            st.session_state.show_reset_page = False
            st.switch_page("pages/forgot_password.py")  # Adjust path as needed
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.show_reset_page = False
            st.switch_page("app.py")  # Adjust path as needed
    
    with col3:
        if st.button("📞 Get Help", use_container_width=True):
            st.session_state.show_reset_page = False
            st.switch_page("pages/contact.py")  # Adjust path as needed
    
    # Security information
    st.markdown("""
        <div class='security-note'>
            <h4 style='margin-top: 0; color: #7c3aed;'>
                🔐 Security Notice
            </h4>
            <p style='margin: 0; color: #333; font-size: 0.95rem;'>
                For your security, password reset links:
            </p>
            <ul style='color: #333; font-size: 0.9rem; margin-bottom: 0;'>
                <li>Expire after 1 hour</li>
                <li>Can only be used once</li>
                <li>Are unique to your account</li>
                <li>Should never be shared with anyone</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Contact support
    st.markdown("""
        <div style='text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(0,0,0,0.1);'>
            <p style='color: #666; font-size: 0.95rem;'>
                Still having trouble? Contact our support team
            </p>
            <p style='color: #333; font-size: 1rem;'>
                📧 <strong>support@talkheal.com</strong> | 📞 <strong>+1 (555) 123-4567</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_rate_limit_page():
    """Display rate limit exceeded page"""
    
    st.markdown("<div class='reset-container'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='warning-container'>
            <h2 style='color: #f59e0b; margin-top: 0;'>
                ⚠️ Too Many Attempts
            </h2>
            <p style='color: #333; font-size: 1.1rem;'>
                For security reasons, we've temporarily limited password reset attempts. 
                Please wait before trying again.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate wait time
    if st.session_state.last_reset_time:
        wait_until = st.session_state.last_reset_time + timedelta(minutes=15)
        remaining = wait_until - datetime.now()
        
        if remaining.total_seconds() > 0:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            
            st.markdown(f"""
                <div class='countdown-timer'>
                    ⏱️ Please wait: {minutes}m {seconds}s
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='help-box'>
            <h3 style='color: #d14a7a; margin-top: 0;'>
                Why am I seeing this?
            </h3>
            <p style='color: #333; line-height: 1.8;'>
                We limit password reset attempts to protect your account from unauthorized access. 
                This is a standard security measure.
            </p>
            <p style='color: #333; line-height: 1.8;'>
                <strong>What you can do:</strong>
            </p>
            <ul style='color: #333; line-height: 1.8;'>
                <li>Wait 15 minutes and try again</li>
                <li>Make sure you're using the correct reset link from your email</li>
                <li>Contact support if you believe this is an error</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Return to Home", use_container_width=True):
        st.switch_page("app.py")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_success_page():
    """Display password reset success page"""
    
    st.markdown("<div class='reset-container'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='success-container'>
            <h2 style='color: #10b981; margin-top: 0; text-align: center;'>
                ✅ Password Reset Successful!
            </h2>
            <p style='color: #333; font-size: 1.1rem; text-align: center;'>
                Your password has been successfully reset. You can now log in with your new password.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='info-container'>
            <h3 style='color: #3b82f6; margin-top: 0;'>
                🔐 Security Recommendations
            </h3>
            <ul style='color: #333; line-height: 1.8;'>
                <li>Use a strong, unique password for your TalkHeal account</li>
                <li>Don't reuse passwords from other websites</li>
                <li>Consider using a password manager</li>
                <li>Enable two-factor authentication if available</li>
                <li>Never share your password with anyone</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔑 Log In Now", use_container_width=True, type="primary"):
            st.switch_page("pages/login.py")  # Adjust path as needed
    
    with col2:
        if st.button("🏠 Go to Home", use_container_width=True):
            st.switch_page("app.py")
    
    st.markdown("""
        <div style='text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(0,0,0,0.1);'>
            <p style='color: #666; font-size: 0.9rem;'>
                If you didn't request this password reset, please contact support immediately.
            </p>
            <p style='color: #333; font-size: 1rem;'>
                📧 <strong>security@talkheal.com</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def check_rate_limit():
    """Check if user has exceeded rate limit for reset attempts"""
    if st.session_state.last_reset_time:
        time_since_last = datetime.now() - st.session_state.last_reset_time
        
        # Reset counter if 15 minutes have passed
        if time_since_last > timedelta(minutes=15):
            st.session_state.reset_attempts = 0
            st.session_state.last_reset_time = None
            return False
        
        # Check if exceeded limit (e.g., 3 attempts per 15 minutes)
        if st.session_state.reset_attempts >= 3:
            return True
    
    return False

def run():
    """Main function to handle password reset flow"""
    
    # Check rate limit first
    if check_rate_limit():
        show_rate_limit_page()
        return
    
    # Check if we should show success page
    if st.session_state.get("reset_successful", False):
        show_success_page()
        return
    
    # Handle token validation
    if st.session_state.show_reset_page and st.session_state.reset_token:
        
        # Validate token if not already checked
        if not st.session_state.token_checked:
            is_valid, error_message = validate_token(st.session_state.reset_token)
            st.session_state.token_checked = True
            st.session_state.token_valid = is_valid
            
            # Track reset attempt
            st.session_state.reset_attempts += 1
            st.session_state.last_reset_time = datetime.now()
            
            if not is_valid:
                # Determine error type and show appropriate page
                if error_message:
                    if "expired" in error_message.lower():
                        show_error_page("expired")
                    elif "used" in error_message.lower():
                        show_error_page("used")
                    else:
                        show_error_page("invalid")
                else:
                    show_error_page("invalid")
                return
        
        # If token is valid, show the reset password form
        if st.session_state.token_valid:
            show_reset_password_page()
        else:
            show_error_page("invalid")
    
    else:
        # No token provided
        show_error_page("no_token")

if __name__ == "__main__":
    run()