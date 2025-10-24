import streamlit as st
import os
from datetime import datetime, timedelta
import json
import random

# Initialize session state
if 'registered_sessions' not in st.session_state:
    st.session_state.registered_sessions = []
if 'favorite_experts' not in st.session_state:
    st.session_state.favorite_experts = []
if 'questions_submitted' not in st.session_state:
    st.session_state.questions_submitted = 0
if 'session_reminders' not in st.session_state:
    st.session_state.session_reminders = {}
if 'question_votes' not in st.session_state:
    st.session_state.question_votes = {}

# Helper Functions
def save_question_to_file(question, category="General", is_anonymous=False):
    """Save submitted question to file with metadata."""
    try:
        if not os.path.exists("data/questions"):
            os.makedirs("data/questions")
        
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        question_data = {
            'question': question,
            'category': category,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'anonymous': is_anonymous,
            'status': 'pending',
            'votes': 0
        }
        
        with open(f"data/questions/question_{now}.json", "w") as f:
            json.dump(question_data, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving question: {e}")
        return False

def load_community_questions():
    """Load all community questions for voting."""
    questions = []
    try:
        if os.path.exists("data/questions"):
            for filename in os.listdir("data/questions"):
                if filename.endswith('.json'):
                    with open(f"data/questions/{filename}", 'r') as f:
                        question_data = json.load(f)
                        question_data['id'] = filename
                        questions.append(question_data)
    except Exception as e:
        st.warning(f"Could not load questions: {e}")
    
    return sorted(questions, key=lambda x: x.get('votes', 0), reverse=True)

def add_to_calendar(session_name, session_date, session_time):
    """Generate calendar event data."""
    return {
        'name': session_name,
        'date': session_date,
        'time': session_time,
        'added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_expert_specializations():
    """Return detailed expert information."""
    return {
        "Dr. Rahul Kumar": {
            "title": "Clinical Psychologist",
            "specialization": "Stress Management, Anxiety, Depression",
            "experience": "15+ years",
            "education": "PhD in Clinical Psychology, Harvard University",
            "languages": "English, Hindi",
            "rating": 4.9,
            "sessions_conducted": 127,
            "image": "static_files/pink.png",
            "bio": "Dr. Rahul specializes in cognitive behavioral therapy and has helped thousands overcome anxiety and stress-related disorders."
        },
        "Dr. Manish Kumar": {
            "title": "Licensed Therapist",
            "specialization": "Relationship Counseling, Family Therapy",
            "experience": "12+ years",
            "education": "MA in Marriage & Family Therapy, Stanford",
            "languages": "English, Hindi, Punjabi",
            "rating": 4.8,
            "sessions_conducted": 98,
            "image": "static_files/mint.png",
            "bio": "Dr. Manish has extensive experience in couples counseling and helping families navigate difficult transitions."
        },
        "Dr. Rajiv Kumar": {
            "title": "Counseling Psychologist",
            "specialization": "Mindfulness, Meditation, Trauma Recovery",
            "experience": "10+ years",
            "education": "PsyD in Counseling Psychology, UCLA",
            "languages": "English, Hindi, Tamil",
            "rating": 4.9,
            "sessions_conducted": 85,
            "image": "static_files/lavender.png",
            "bio": "Dr. Rajiv combines traditional therapy with mindfulness practices to help clients achieve lasting peace and recovery."
        }
    }

def get_upcoming_sessions():
    """Return list of upcoming sessions."""
    return [
        {
            "name": "Navigating Stress in the Digital Age",
            "expert": "Dr. Rahul Kumar",
            "date": "October 15, 2025",
            "time": "6:00 PM GMT",
            "duration": "60 minutes",
            "spots_left": 15,
            "description": "Join Dr. Rahul Kumar for a live Q&A on managing stress and digital fatigue.",
            "topics": ["Digital Detox", "Work-Life Balance", "Stress Management"],
            "registered": 35
        },
        {
            "name": "Building Healthy Relationships",
            "expert": "Dr. Manish Kumar",
            "date": "October 22, 2025",
            "time": "7:00 PM GMT",
            "duration": "90 minutes",
            "spots_left": 8,
            "description": "Learn effective communication strategies and conflict resolution techniques.",
            "topics": ["Communication", "Conflict Resolution", "Trust Building"],
            "registered": 42
        },
        {
            "name": "Mindfulness for Beginners",
            "expert": "Dr. Rajiv Kumar",
            "date": "October 29, 2025",
            "time": "5:30 PM GMT",
            "duration": "45 minutes",
            "spots_left": 25,
            "description": "Introduction to mindfulness meditation and its benefits for mental health.",
            "topics": ["Meditation Basics", "Breathing Techniques", "Daily Practice"],
            "registered": 25
        }
    ]

def get_past_sessions():
    """Return list of past sessions with recordings."""
    return [
        {
            "name": "Understanding Anxiety",
            "expert": "Dr. Rahul Kumar",
            "date": "September 15, 2025",
            "video_url": "https://www.youtube.com/watch?v=G0zJGDokyA",
            "description": "A comprehensive guide to understanding and managing anxiety disorders.",
            "duration": "55 minutes",
            "views": 1247,
            "rating": 4.8
        },
        {
            "name": "Mindfulness and Meditation Techniques",
            "expert": "Dr. Rajiv Kumar",
            "date": "September 8, 2025",
            "video_url": "https://www.youtube.com/watch?v=O-6f5wQXSu8",
            "description": "Learn simple mindfulness and meditation techniques to calm your mind.",
            "duration": "42 minutes",
            "views": 892,
            "rating": 4.9
        },
        {
            "name": "Managing Depression",
            "expert": "Dr. Rahul Kumar",
            "date": "August 25, 2025",
            "video_url": "https://www.youtube.com/watch?v=z-IR48Mb3W0",
            "description": "Understanding depression symptoms and effective coping strategies.",
            "duration": "62 minutes",
            "views": 1534,
            "rating": 4.7
        },
        {
            "name": "Sleep and Mental Health",
            "expert": "Dr. Manish Kumar",
            "date": "August 18, 2025",
            "video_url": "https://www.youtube.com/watch?v=EiYm20F9WXU",
            "description": "The crucial connection between quality sleep and mental well-being.",
            "duration": "48 minutes",
            "views": 678,
            "rating": 4.6
        }
    ]

def show():
    # Page Header
    st.markdown("""
        <div style='background: var(--secondary-background-color); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(0,0,0,0.1); padding: 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='text-align: center; font-family: "Helvetica Neue", sans-serif;'>Expert-Led Q&A Sessions</h2>
            <p style='font-size: 1.1rem; text-align: center;'>
                Connect with licensed mental health professionals, gain valuable insights, and get your questions answered in our expert-led sessions.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Quick Stats
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    with stats_col1:
        st.metric("Sessions Conducted", "310+")
    with stats_col2:
        st.metric("Active Experts", "3")
    with stats_col3:
        st.metric("Participants", "2,500+")
    with stats_col4:
        st.metric("Avg. Rating", "4.8 ⭐")

    st.markdown("---")

    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Upcoming Sessions",
        "👥 Meet Our Experts",
        "📹 Past Sessions",
        "❓ Ask Questions",
        "💬 Community Q&A"
    ])

    # Tab 1: Upcoming Sessions
    with tab1:
        st.markdown("<h3 style='text-align: center;'>Upcoming Sessions</h3>", unsafe_allow_html=True)
        
        # Filter options
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            topic_filter = st.selectbox(
                "Filter by Topic",
                ["All Topics", "Stress Management", "Relationships", "Mindfulness", "Depression", "Anxiety"]
            )
        with filter_col2:
            expert_filter = st.selectbox(
                "Filter by Expert",
                ["All Experts", "Dr. Rahul Kumar", "Dr. Manish Kumar", "Dr. Rajiv Kumar"]
            )
        
        upcoming_sessions = get_upcoming_sessions()
        
        for session in upcoming_sessions:
            with st.container():
                st.markdown(f"""
                    <div style='background-color: var(--secondary-background-color); border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 2rem; margin-bottom: 2rem;'>
                        <h4>{session['name']}</h4>
                        <p><b>Expert:</b> {session['expert']}</p>
                        <p>{session['description']}</p>
                        <p><b>📅 Date:</b> {session['date']}</p>
                        <p><b>🕐 Time:</b> {session['time']}</p>
                        <p><b>⏱️ Duration:</b> {session['duration']}</p>
                        <p><b>👥 Registered:</b> {session['registered']} participants</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Topics
                st.markdown("**Topics Covered:**")
                topic_cols = st.columns(len(session['topics']))
                for idx, topic in enumerate(session['topics']):
                    with topic_cols[idx]:
                        st.info(topic)
                
                # Registration button
                button_col1, button_col2, button_col3 = st.columns([2, 1, 1])
                with button_col1:
                    if session['name'] in st.session_state.registered_sessions:
                        st.success("✅ You are registered for this session!")
                    else:
                        if st.button(f"Register Now ({session['spots_left']} spots left)", key=f"register_{session['name']}"):
                            st.session_state.registered_sessions.append(session['name'])
                            st.success("Successfully registered! You'll receive a reminder before the session.")
                            st.balloons()
                            st.rerun()
                
                with button_col2:
                    if st.button("📅 Add to Calendar", key=f"calendar_{session['name']}"):
                        st.session_state.session_reminders[session['name']] = add_to_calendar(
                            session['name'],
                            session['date'],
                            session['time']
                        )
                        st.success("Added to your reminders!")
                
                with button_col3:
                    if st.button("🔔 Notify Me", key=f"notify_{session['name']}"):
                        st.info("You'll receive a notification 1 hour before the session!")
                
                st.markdown("---")
        
        # My Registered Sessions
        if st.session_state.registered_sessions:
            st.markdown("### 📋 Your Registered Sessions")
            for session_name in st.session_state.registered_sessions:
                st.success(f"✅ {session_name}")

    # Tab 2: Meet Our Experts
    with tab2:
        st.markdown("<h3 style='text-align: center;'>Meet Our Experts</h3>", unsafe_allow_html=True)
        
        experts = get_expert_specializations()
        
        for expert_name, expert_info in experts.items():
            with st.expander(f"👨‍⚕️ {expert_name} - {expert_info['title']}", expanded=False):
                expert_col1, expert_col2 = st.columns([1, 2])
                
                with expert_col1:
                    st.image(expert_info['image'], width=200)
                    
                    # Favorite button
                    if expert_name in st.session_state.favorite_experts:
                        if st.button(f"⭐ Favorited", key=f"fav_{expert_name}"):
                            st.session_state.favorite_experts.remove(expert_name)
                            st.rerun()
                    else:
                        if st.button(f"☆ Add to Favorites", key=f"fav_{expert_name}"):
                            st.session_state.favorite_experts.append(expert_name)
                            st.success("Added to favorites!")
                            st.rerun()
                
                with expert_col2:
                    st.markdown(f"**{expert_info['title']}**")
                    st.write(expert_info['bio'])
                    
                    st.markdown("---")
                    
                    info_col1, info_col2 = st.columns(2)
                    with info_col1:
                        st.write(f"**🎓 Education:**")
                        st.write(expert_info['education'])
                        st.write(f"**💼 Experience:**")
                        st.write(expert_info['experience'])
                    
                    with info_col2:
                        st.write(f"**🏆 Specialization:**")
                        st.write(expert_info['specialization'])
                        st.write(f"**🌍 Languages:**")
                        st.write(expert_info['languages'])
                    
                    st.markdown("---")
                    
                    metric_col1, metric_col2 = st.columns(2)
                    with metric_col1:
                        st.metric("Rating", f"{expert_info['rating']}/5.0 ⭐")
                    with metric_col2:
                        st.metric("Sessions", expert_info['sessions_conducted'])
        
        # Favorite Experts
        if st.session_state.favorite_experts:
            st.markdown("### ⭐ Your Favorite Experts")
            for expert in st.session_state.favorite_experts:
                st.info(f"⭐ {expert}")

    # Tab 3: Past Sessions
    with tab3:
        st.markdown("<h3>Past Sessions Library</h3>", unsafe_allow_html=True)
        st.write("Browse recordings from our previous expert-led sessions.")
        
        # Search and filter
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_query = st.text_input("🔍 Search past sessions", placeholder="e.g., anxiety, meditation, depression")
        with search_col2:
            sort_by = st.selectbox("Sort by", ["Most Recent", "Most Viewed", "Highest Rated"])
        
        past_sessions = get_past_sessions()
        
        # Sort sessions
        if sort_by == "Most Viewed":
            past_sessions = sorted(past_sessions, key=lambda x: x['views'], reverse=True)
        elif sort_by == "Highest Rated":
            past_sessions = sorted(past_sessions, key=lambda x: x['rating'], reverse=True)
        
        for session in past_sessions:
            # Filter by search query
            if search_query and search_query.lower() not in session['name'].lower():
                continue
            
            with st.container():
                st.markdown(f"<h4>{session['name']}</h4>", unsafe_allow_html=True)
                
                video_col1, video_col2 = st.columns([2, 1])
                
                with video_col1:
                    st.video(session['video_url'])
                
                with video_col2:
                    st.write(f"**👨‍⚕️ Expert:** {session['expert']}")
                    st.write(f"**📅 Date:** {session['date']}")
                    st.write(f"**⏱️ Duration:** {session['duration']}")
                    st.write(f"**👁️ Views:** {session['views']:,}")
                    st.write(f"**⭐ Rating:** {session['rating']}/5.0")
                    
                    if st.button("📥 Download Notes", key=f"notes_{session['name']}"):
                        st.info("Session notes will be available soon!")
                
                st.markdown(session['description'])
                st.markdown("---")

    # Tab 4: Ask Questions
    with tab4:
        st.markdown("<h3>Submit a Question</h3>", unsafe_allow_html=True)
        st.write("Have a question for our experts? Submit it here and we might answer it in our next session.")
        
        question_col1, question_col2 = st.columns([3, 1])
        
        with question_col1:
            question_category = st.selectbox(
                "Question Category",
                ["General", "Anxiety", "Depression", "Stress", "Relationships", "Sleep", "Mindfulness", "Other"]
            )
            
            question = st.text_area(
                "Your Question",
                height=150,
                placeholder="Type your question here..."
            )
            
            is_anonymous = st.checkbox("Submit anonymously", value=False)
            
            if st.button("Submit Question", type="primary"):
                if question:
                    if save_question_to_file(question, question_category, is_anonymous):
                        st.session_state.questions_submitted += 1
                        st.success("Thank you for your submission! Our experts will review it soon.")
                        st.balloons()
                    else:
                        st.error("Failed to submit question. Please try again.")
                else:
                    st.warning("Please enter a question before submitting.")
        
        with question_col2:
            st.info("**💡 Tips for Good Questions:**")
            st.write("• Be specific")
            st.write("• Provide context")
            st.write("• Keep it concise")
            st.write("• Stay respectful")
            
            if st.session_state.questions_submitted > 0:
                st.metric("Questions Submitted", st.session_state.questions_submitted)
        
        st.markdown("---")
        
        # FAQ Section
        st.markdown("### 🔥 Frequently Asked Questions")
        
        common_questions = [
            {
                "q": "How do I know if I need therapy?",
                "a": "If you're experiencing persistent sadness, anxiety, or difficulty coping with daily life, therapy can help. It's also beneficial for personal growth and self-discovery.",
                "expert": "Dr. Rahul Kumar"
            },
            {
                "q": "What's the difference between a psychologist and psychiatrist?",
                "a": "Psychologists provide talk therapy and behavioral interventions. Psychiatrists are medical doctors who can prescribe medication and often focus on the biological aspects of mental health.",
                "expert": "Dr. Manish Kumar"
            },
            {
                "q": "How can I practice mindfulness daily?",
                "a": "Start with just 5 minutes of focused breathing each morning. Gradually increase duration. Use mindfulness apps, and practice being present during routine activities like eating or walking.",
                "expert": "Dr. Rajiv Kumar"
            }
        ]
        
        for idx, faq in enumerate(common_questions):
            with st.expander(f"❓ {faq['q']}"):
                st.write(faq['a'])
                st.caption(f"— {faq['expert']}")

    # Tab 5: Community Q&A
    with tab5:
        st.markdown("<h3>Community Q&A</h3>", unsafe_allow_html=True)
        st.write("Vote on questions from the community. The most popular questions will be answered in upcoming sessions!")
        
        community_questions = load_community_questions()
        
        if not community_questions:
            st.info("No community questions yet. Be the first to submit one!")
        else:
            st.write(f"**Total Community Questions:** {len(community_questions)}")
            
            for question in community_questions[:10]:  # Show top 10
                with st.container():
                    q_col1, q_col2 = st.columns([5, 1])
                    
                    with q_col1:
                        if question.get('anonymous', False):
                            st.markdown(f"**👤 Anonymous** • {question.get('category', 'General')}")
                        else:
                            st.markdown(f"**Category:** {question.get('category', 'General')}")
                        
                        st.write(question['question'])
                        st.caption(f"Submitted: {question.get('timestamp', 'Unknown')}")
                    
                    with q_col2:
                        question_id = question.get('id', '')
                        current_votes = st.session_state.question_votes.get(question_id, question.get('votes', 0))
                        
                        if st.button(f"👍 {current_votes}", key=f"vote_{question_id}"):
                            st.session_state.question_votes[question_id] = current_votes + 1
                            st.success("Voted!")
                            st.rerun()
                    
                    st.markdown("---")

    # Footer: Contact & Support
    st.markdown("---")
    st.markdown("""
        <div style='background-color: var(--secondary-background-color); border-radius: 10px; padding: 1.5rem; text-align: center;'>
            <h4>Need Immediate Support?</h4>
            <p>If you're in crisis, please contact emergency services or call a mental health hotline immediately.</p>
            <p><b>Crisis Hotline:</b> 1-800-273-8255 (Available 24/7)</p>
        </div>
    """, unsafe_allow_html=True)

show()

