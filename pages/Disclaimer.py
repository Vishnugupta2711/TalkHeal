import streamlit as st
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
        
        /* Enhanced disclaimer styles */
        .disclaimer-section {{
            background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%);
            border-radius: 18px;
            box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12);
            padding: 2.5rem 2.5rem 2rem 2.5rem;
            margin: 2rem auto;
            max-width: 900px;
        }}
        
        .warning-box {{
            background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
            border-left: 5px solid #d14a7a;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(209,74,122,0.1);
        }}
        
        .info-box {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border-left: 5px solid #3b82f6;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(59,130,246,0.1);
        }}
        
        .emergency-box {{
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border: 2px solid #dc2626;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 12px rgba(220,38,38,0.15);
        }}
        
        .section-divider {{
            height: 2px;
            background: linear-gradient(90deg, transparent, #d14a7a, transparent);
            margin: 2rem 0;
            border: none;
        }}
        
        .disclaimer-icon {{
            display: inline-block;
            font-size: 1.4rem;
            margin-right: 0.5rem;
            vertical-align: middle;
        }}
        
        .contact-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}
        
        .accordion-item {{
            background: white;
            margin: 1rem 0;
            border-radius: 10px;
            padding: 1rem 1.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .accordion-item:hover {{
            box-shadow: 0 4px 12px rgba(209,74,122,0.15);
            transform: translateY(-2px);
        }}
        
        .resource-link {{
            display: inline-block;
            background: linear-gradient(135deg, #d14a7a 0%, #c13d6e 100%);
            color: white !important;
            padding: 0.7rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            margin: 0.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(209,74,122,0.2);
        }}
        
        .resource-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(209,74,122,0.3);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set your background image
selected_palette = st.session_state.get("palette_name", "Pink")
set_background_for_theme(selected_palette)


def show():
    st.markdown("""
        <div class='disclaimer-section'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive; text-align: center; margin-bottom: 2rem;'>
                <span class='disclaimer-icon'>⚠️</span> Important Legal Disclaimer
            </h2>
    """, unsafe_allow_html=True)
    
    # Main disclaimer
    st.markdown("""
            <div style='color: #222; font-size: 1.1rem; line-height: 1.8;'>
                <p><b>Please Read Carefully Before Using TalkHeal</b></p>
                <p>
                    TalkHeal is designed to provide support, resources, and information for mental wellness and personal development. 
                    However, it is <b>not a substitute</b> for professional medical advice, diagnosis, or treatment from qualified healthcare providers.
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Medical Advice Section
    st.markdown("""
            <div class='warning-box'>
                <h3 style='color: #d14a7a; margin-top: 0;'>
                    <span class='disclaimer-icon'>🏥</span> Not Medical Advice
                </h3>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li>Always seek the advice of your physician or qualified health provider with any questions regarding a medical condition</li>
                    <li>Never disregard professional medical advice or delay seeking it because of information from TalkHeal</li>
                    <li>The content provided is for informational and educational purposes only</li>
                    <li>TalkHeal does not provide diagnosis, treatment recommendations, or prescriptions</li>
                    <li>Individual results may vary - what works for one person may not work for another</li>
                </ul>
            </div>
    """, unsafe_allow_html=True)
    
    # Emergency Section
    st.markdown("""
            <div class='emergency-box'>
                <h3 style='color: #dc2626; margin-top: 0;'>
                    <span class='disclaimer-icon'>🚨</span> Emergency & Crisis Support
                </h3>
                <p style='color: #333; font-size: 1.05rem; line-height: 1.8;'>
                    <b>If you are experiencing a mental health emergency or having thoughts of harming yourself or others:</b>
                </p>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li><b>Call emergency services immediately (911 in US, 112 in EU, 999 in UK)</b></li>
                    <li>Contact the National Suicide Prevention Lifeline: <b>988</b> (US)</li>
                    <li>Text "HELLO" to <b>741741</b> (Crisis Text Line)</li>
                    <li>Go to your nearest emergency room</li>
                    <li>Contact your mental health provider's emergency line</li>
                </ul>
                <p style='color: #dc2626; font-weight: bold; font-size: 1.1rem; margin-top: 1rem;'>
                    ⚠️ TalkHeal is NOT equipped to handle emergency situations
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Limitation of Liability
    st.markdown("""
            <div class='info-box'>
                <h3 style='color: #3b82f6; margin-top: 0;'>
                    <span class='disclaimer-icon'>⚖️</span> Limitation of Liability
                </h3>
                <p style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    TalkHeal and its creators, affiliates, partners, and employees are <b>not responsible or liable</b> for:
                </p>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li>Any decisions, actions, or outcomes based on information provided through this platform</li>
                    <li>The accuracy, completeness, or timeliness of any content</li>
                    <li>Any damages, losses, or injuries resulting from use of TalkHeal</li>
                    <li>Third-party content, links, or resources provided on the platform</li>
                    <li>Technical issues, data loss, or service interruptions</li>
                </ul>
                <p style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <b>Use of this platform constitutes acceptance of these limitations.</b>
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    # Privacy & Data
    st.markdown("""
            <div class='info-box'>
                <h3 style='color: #3b82f6; margin-top: 0;'>
                    <span class='disclaimer-icon'>🔒</span> Privacy & Data Security
                </h3>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li>We take your privacy seriously and use encryption to protect your data</li>
                    <li>Your conversations and personal information are confidential within legal limits</li>
                    <li>We may share information if required by law or to prevent imminent harm</li>
                    <li>Review our full Privacy Policy for detailed information on data handling</li>
                    <li>You have the right to request deletion of your data at any time</li>
                </ul>
            </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # AI & Technology Disclaimer
    st.markdown("""
            <div class='warning-box'>
                <h3 style='color: #d14a7a; margin-top: 0;'>
                    <span class='disclaimer-icon'>🤖</span> AI-Powered Features
                </h3>
                <p style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    TalkHeal may use artificial intelligence and automated systems:
                </p>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li>AI responses are generated by algorithms and may contain errors or biases</li>
                    <li>AI cannot replace human judgment, empathy, or professional expertise</li>
                    <li>Always verify important information with qualified professionals</li>
                    <li>We continuously improve our AI, but it has limitations</li>
                    <li>Report any concerning or inappropriate AI responses to our team</li>
                </ul>
            </div>
    """, unsafe_allow_html=True)
    
    # Age & Eligibility
    st.markdown("""
            <div class='info-box'>
                <h3 style='color: #3b82f6; margin-top: 0;'>
                    <span class='disclaimer-icon'>👥</span> User Eligibility
                </h3>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li>Users must be at least 13 years old to use TalkHeal</li>
                    <li>Users under 18 should have parental/guardian consent</li>
                    <li>Parents/guardians are responsible for monitoring minors' use of the platform</li>
                    <li>Some features may have additional age or eligibility requirements</li>
                </ul>
            </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Professional Credentials
    st.markdown("""
            <div class='warning-box'>
                <h3 style='color: #d14a7a; margin-top: 0;'>
                    <span class='disclaimer-icon'>📋</span> Professional Credentials
                </h3>
                <p style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    If TalkHeal connects you with mental health professionals:
                </p>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li>Always verify the credentials and licensing of any professional</li>
                    <li>Ensure they are licensed to practice in your jurisdiction</li>
                    <li>We provide a platform but do not guarantee the qualifications of third-party providers</li>
                    <li>Report any concerns about professional conduct to us immediately</li>
                </ul>
            </div>
    """, unsafe_allow_html=True)
    
    # Content Accuracy
    st.markdown("""
            <div class='info-box'>
                <h3 style='color: #3b82f6; margin-top: 0;'>
                    <span class='disclaimer-icon'>✓</span> Content Accuracy & Updates
                </h3>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li>We strive to provide accurate, evidence-based information</li>
                    <li>Mental health research evolves - some content may become outdated</li>
                    <li>Content is reviewed but may contain errors or omissions</li>
                    <li>We update content regularly but cannot guarantee real-time accuracy</li>
                    <li>Always consult multiple sources for important decisions</li>
                </ul>
            </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # International Use
    st.markdown("""
            <div class='info-box'>
                <h3 style='color: #3b82f6; margin-top: 0;'>
                    <span class='disclaimer-icon'>🌍</span> International Use
                </h3>
                <p style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    TalkHeal may be accessed internationally:
                </p>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li>Content may not comply with laws or regulations in all jurisdictions</li>
                    <li>Emergency resources and hotlines are primarily US-focused</li>
                    <li>Users are responsible for compliance with local laws</li>
                    <li>Mental health practices and cultural norms vary by region</li>
                </ul>
            </div>
    """, unsafe_allow_html=True)
    
    # Changes to Disclaimer
    st.markdown("""
            <div class='warning-box'>
                <h3 style='color: #d14a7a; margin-top: 0;'>
                    <span class='disclaimer-icon'>📝</span> Changes to This Disclaimer
                </h3>
                <p style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    We reserve the right to modify this disclaimer at any time. Changes will be effective immediately upon posting. 
                    Your continued use of TalkHeal constitutes acceptance of any modifications.
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Contact Section
    st.markdown("""
            <div class='contact-card'>
                <h3 style='color: #d14a7a; margin-top: 0;'>
                    <span class='disclaimer-icon'>📧</span> Questions or Concerns?
                </h3>
                <p style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    If you have questions about this disclaimer or need to report an issue:
                </p>
                <ul style='color: #333; font-size: 1rem; line-height: 1.8;'>
                    <li><b>Email:</b> support@talkheal.com</li>
                    <li><b>Legal Inquiries:</b> legal@talkheal.com</li>
                    <li><b>Privacy Concerns:</b> privacy@talkheal.com</li>
                    <li><b>Phone:</b> +1 (555) 123-4567 (Mon-Fri, 9 AM - 5 PM EST)</li>
                </ul>
            </div>
    """, unsafe_allow_html=True)
    
    # Quick Links
    st.markdown("""
            <div style='text-align: center; margin: 2rem 0;'>
                <h3 style='color: #d14a7a;'>Related Resources</h3>
                <a href='#' class='resource-link'>Privacy Policy</a>
                <a href='#' class='resource-link'>Terms of Service</a>
                <a href='#' class='resource-link'>Community Guidelines</a>
                <a href='#' class='resource-link'>FAQ</a>
            </div>
    """, unsafe_allow_html=True)
    
    # Acknowledgment
    st.markdown("""
            <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 2rem 0; text-align: center;'>
                <p style='color: #666; font-size: 0.95rem; margin: 0;'>
                    <b>By using TalkHeal, you acknowledge that you have read, understood, and agree to this disclaimer.</b>
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    # Last Updated
    st.markdown("""
            <div style='text-align: center; color: #999; font-size: 0.9rem; margin-top: 2rem;'>
                <i>Last updated: September 2025 • Version 2.0</i><br>
                <i>Effective Date: September 1, 2025</i>
            </div>
        </div>
    """, unsafe_allow_html=True)

show()