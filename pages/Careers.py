import streamlit as st
import os
from datetime import datetime
import re

def show():
    st.markdown("""        <style>
            .career-container {
                background-color: var(--secondary-background-color);
                color: var(--text-color);
                padding: 2rem;
                border-radius: 10px;
                margin: 2rem auto;
                max-width: 900px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .opening-item {
                padding: 1rem;
                border-radius: 8px;
                transition: all 0.3s;
                border-left: 4px solid transparent;
                margin: 0.5rem 0;
                background-color: rgba(255,255,255,0.05);
            }
            .opening-item:hover {
                background-color: rgba(0,0,0,0.08);
                border-left-color: #4CAF50;
                transform: translateX(5px);
            }
            .benefit-card {
                background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(33, 150, 243, 0.1));
                padding: 1rem;
                border-radius: 8px;
                margin: 0.5rem 0;
                border-left: 3px solid #4CAF50;
            }
            .stats-box {
                text-align: center;
                padding: 1.5rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
                color: white;
                margin: 1rem 0;
            }
            .job-detail {
                background-color: rgba(0,0,0,0.03);
                padding: 1rem;
                border-radius: 5px;
                margin: 0.5rem 0;
            }
            .requirement-item {
                padding: 0.3rem 0;
                padding-left: 1.5rem;
                position: relative;
            }
            .requirement-item:before {
                content: "✓";
                position: absolute;
                left: 0;
                color: #4CAF50;
                font-weight: bold;
            }
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

    st.markdown("<div class='career-container'>", unsafe_allow_html=True)
    
    st.header("🚀 Careers at TalkHeal")
    st.write("Join our mission to support mental wellness and make a real impact!")
    
    # Company culture section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='stats-box'><h3>50+</h3><p>Team Members</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stats-box'><h3>Remote</h3><p>Work Flexibility</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='stats-box'><h3>Growing</h3><p>Fast Scaling</p></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Benefits section
    st.subheader("💼 Why Join TalkHeal?")
    
    benefits = [
        ("🏥", "Comprehensive Health Insurance", "Medical, dental, and mental health coverage"),
        ("🌴", "Flexible Work Schedule", "Work-life balance with remote options"),
        ("📚", "Learning & Development", "Professional growth opportunities and courses"),
        ("💰", "Competitive Compensation", "Market-leading salary and equity options"),
        ("🎯", "Impact-Driven Mission", "Make a real difference in people's lives"),
        ("🤝", "Inclusive Culture", "Diverse, supportive, and collaborative environment")
    ]
    
    cols = st.columns(2)
    for idx, (icon, title, desc) in enumerate(benefits):
        with cols[idx % 2]:
            st.markdown(f"<div class='benefit-card'><strong>{icon} {title}</strong><br><small>{desc}</small></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📋 Current Openings")
    
    # Enhanced job openings with details
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
        "Community Manager": {
            "icon": "🤝",
            "type": "Full-time",
            "location": "Remote / Hybrid",
            "experience": "2-4 years",
            "description": "Build and nurture our mental health community",
            "responsibilities": [
                "Engage with community members across platforms",
                "Organize virtual events and support groups",
                "Moderate discussions and ensure safe spaces",
                "Collaborate with mental health professionals"
            ]
        },
        "Content Writer (Mental Health)": {
            "icon": "✍️",
            "type": "Full-time",
            "location": "Remote",
            "experience": "1-3 years",
            "description": "Create empathetic, evidence-based mental health content",
            "responsibilities": [
                "Write blog posts, articles, and resources",
                "Research mental health topics and trends",
                "Collaborate with therapists for accuracy",
                "Develop engaging social media content"
            ]
        },
        "Full Stack Developer": {
            "icon": "💻",
            "type": "Full-time",
            "location": "Remote / On-site",
            "experience": "3-5 years",
            "description": "Build scalable mental health tech solutions",
            "responsibilities": [
                "Develop and maintain web applications",
                "Implement secure, HIPAA-compliant features",
                "Work with React, Node.js, and Python",
                "Collaborate with cross-functional teams"
            ]
        },
        "UI/UX Designer": {
            "icon": "🎨",
            "type": "Full-time",
            "location": "Remote / Hybrid",
            "experience": "2-4 years",
            "description": "Design compassionate, user-centered experiences",
            "responsibilities": [
                "Create intuitive interfaces for mental health apps",
                "Conduct user research and usability testing",
                "Design accessible and inclusive experiences",
                "Maintain design systems and guidelines"
            ]
        }
    }
    
    # Job listing selector
    selected_job = st.selectbox("Select a position to view details:", ["View all positions"] + list(openings.keys()))
    
    if selected_job == "View all positions":
        for job_title, details in openings.items():
            with st.expander(f"{details['icon']} {job_title} - {details['type']}"):
                st.markdown(f"**📍 Location:** {details['location']}")
                st.markdown(f"**⏱️ Experience:** {details['experience']}")
                st.markdown(f"**📝 Description:** {details['description']}")
                
                st.markdown("**Key Responsibilities:**")
                for resp in details['responsibilities']:
                    st.markdown(f"<div class='requirement-item'>{resp}</div>", unsafe_allow_html=True)
    else:
        details = openings[selected_job]
        st.markdown(f"<div class='job-detail'>", unsafe_allow_html=True)
        st.markdown(f"### {details['icon']} {selected_job}")
        st.markdown(f"**Type:** {details['type']} | **Location:** {details['location']} | **Experience:** {details['experience']}")
        st.markdown(f"\n**About the role:**\n{details['description']}")
        
        st.markdown("\n**Key Responsibilities:**")
        for resp in details['responsibilities']:
            st.markdown(f"<div class='requirement-item'>{resp}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.subheader("📝 Apply Now")
    
    with st.form("application_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            phone = st.text_input("Phone Number", placeholder="+1 (555) 000-0000")
        
        with col2:
            position = st.selectbox("Position *", options=list(openings.keys()))
            experience_years = st.selectbox("Years of Experience *", ["0-1", "1-3", "3-5", "5-10", "10+"])
            linkedin = st.text_input("LinkedIn Profile", placeholder="https://linkedin.com/in/yourprofile")
        
        portfolio = st.text_input("Portfolio/GitHub (if applicable)", placeholder="https://yourportfolio.com")
        
        resume = st.file_uploader("Upload Your Resume *", type=["pdf", "docx"], help="Max file size: 10MB")
        
        # Availability
        availability = st.selectbox("When can you start?", 
                                   ["Immediately", "Within 2 weeks", "Within 1 month", "Within 2-3 months", "Other"])
        
        # Salary expectation
        salary_expectation = st.text_input("Salary Expectation (Optional)", placeholder="e.g., $80,000 - $100,000")
        
        cover_letter = st.text_area("Cover Letter (Optional)", 
                                    placeholder="Tell us why you're excited about this role and what makes you a great fit...",
                                    height=150)
        
        # Consent checkbox
        consent = st.checkbox("I agree to the processing of my personal data for recruitment purposes *")
        
        # Additional questions
        hear_about = st.multiselect("How did you hear about us?", 
                                    ["LinkedIn", "Job Board", "Referral", "Company Website", "Social Media", "Other"])
        
        submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True)
        
        if submitted:
            # Validation
            def is_valid_email(email):
                return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None
            
            errors = []
            
            if not name:
                errors.append("Full Name is required")
            if not email:
                errors.append("Email Address is required")
            elif not is_valid_email(email):
                errors.append("Please enter a valid email address")
            if not position:
                errors.append("Position is required")
            if not resume:
                errors.append("Resume is required")
            if not consent:
                errors.append("You must agree to data processing to continue")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create a directory for applications if it doesn't exist

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
            # Validation
            def is_valid_email(email):
                return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None
            
            errors = []
            
            if not name:
                errors.append("Full Name is required")
            if not email:
                errors.append("Email Address is required")
            elif not is_valid_email(email):
                errors.append("Please enter a valid email address")
            if not position:
                errors.append("Position is required")
            if not resume:
                errors.append("Resume is required")
            if not consent:
                errors.append("You must agree to data processing to continue")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create a directory for applications if it doesn't exist
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
                    f.write(f"APPLICATION DETAILS\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(f"Name: {name}\n")
                    f.write(f"Email: {email}\n")
                    f.write(f"Phone: {phone}\n")
                    f.write(f"Position: {position}\n")
                    f.write(f"Experience: {experience_years}\n")
                    f.write(f"LinkedIn: {linkedin}\n")
                    f.write(f"Portfolio/GitHub: {portfolio}\n")
                    f.write(f"Availability: {availability}\n")
                    f.write(f"Salary Expectation: {salary_expectation}\n")
                    f.write(f"Heard about us: {', '.join(hear_about)}\n")
                    f.write(f"Application Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(f"COVER LETTER\n")
                    f.write(f"{'-'*50}\n")
                    f.write(f"{cover_letter if cover_letter else 'No cover letter provided.'}\n")
                    
                st.success("✅ Your application has been submitted successfully! We will review it and get back to you within 5-7 business days.")
                st.balloons()
                
                # Display confirmation
                st.info(f"📧 A confirmation email will be sent to {email}")

    st.markdown("---")
    
    # FAQ Section
    with st.expander("❓ Frequently Asked Questions"):
        st.markdown("""
        **Q: What's the hiring process like?**  
        A: Initial screening → Technical/skills assessment → Team interview → Final interview → Offer
        
        **Q: Do you offer remote work?**  
        A: Yes! Most positions offer remote or hybrid options.
        
        **Q: What's the company culture like?**  
        A: We prioritize mental health, work-life balance, and a supportive, inclusive environment.
        
        **Q: Do you sponsor work visas?**  
        A: We evaluate visa sponsorship on a case-by-case basis for exceptional candidates.
        
        **Q: How long does the hiring process take?**  
        A: Typically 2-4 weeks from application to offer.
        """)
    
    # Contact section
    st.markdown("---")
    st.markdown("### 📬 Questions About Careers?")
    st.write("Reach out to our HR team at **careers@talkheal.com** or call us at **+1 (555) 123-4567**")
    
    st.info("💡 **Tip:** Even if you don't see a perfect match, we'd love to hear from you! Send us your resume for future opportunities.")
    
    st.markdown("</div>", unsafe_allow_html=True)

show()


                    f.write(f"Cover Letter:\n{cover_letter}")

show()


    st.info("More roles and opportunities coming soon!")
    
show()
