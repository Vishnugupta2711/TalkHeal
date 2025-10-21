"""
Therapy Preparation & Session Notes Tool
Helps users prepare for therapy sessions by organizing thoughts, tracking topics,
noting questions, and recording post-session insights and homework.
Maximizes effectiveness of professional therapy.
"""

import streamlit as st
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional

# Pre-session preparation prompts
PREPARATION_PROMPTS = {
    "What went well": {
        "icon": "✨",
        "prompt": "What went well this week?",
        "help": "Reflect on positive moments, successes, or progress you've made"
    },
    "Challenges faced": {
        "icon": "⚠️",
        "prompt": "What challenges did I face?",
        "help": "Identify difficulties, struggles, or setbacks you experienced"
    },
    "Emotional state": {
        "icon": "💭",
        "prompt": "How have I been feeling emotionally?",
        "help": "Describe your overall mood and emotional patterns"
    },
    "Important events": {
        "icon": "📅",
        "prompt": "What important events happened?",
        "help": "Note significant occurrences, conversations, or experiences"
    },
    "Patterns noticed": {
        "icon": "🔍",
        "prompt": "What patterns or triggers did I notice?",
        "help": "Identify recurring thoughts, behaviors, or situations"
    },
    "Progress on goals": {
        "icon": "🎯",
        "prompt": "Progress on previous goals or homework?",
        "help": "Review what you worked on since last session"
    }
}

# Questions to ask therapist categories
QUESTION_CATEGORIES = [
    "About my diagnosis/condition",
    "About treatment options",
    "About coping strategies",
    "About medication",
    "About relationships",
    "About my progress",
    "About therapy process",
    "Other"
]

# Post-session reflection prompts
POST_SESSION_PROMPTS = {
    "Key insights": {
        "icon": "💡",
        "prompt": "What were the key insights or 'aha' moments?",
        "help": "What did you learn or realize during the session?"
    },
    "Therapist feedback": {
        "icon": "👥",
        "prompt": "What did my therapist say or suggest?",
        "help": "Important points, observations, or advice from your therapist"
    },
    "Homework assigned": {
        "icon": "📝",
        "prompt": "What homework or tasks were assigned?",
        "help": "Specific actions or exercises to practice before next session"
    },
    "How I'm feeling": {
        "icon": "💫",
        "prompt": "How am I feeling after the session?",
        "help": "Your emotional state and thoughts post-session"
    },
    "Questions arose": {
        "icon": "❓",
        "prompt": "What new questions came up?",
        "help": "Things to explore or ask about next time"
    }
}

# Homework status options
HOMEWORK_STATUS = ["Not Started", "In Progress", "Completed", "Struggled With"]


def initialize_therapy_state():
    """Initialize session state for therapy tool."""
    if "therapy_sessions" not in st.session_state:
        st.session_state.therapy_sessions = load_therapy_sessions()
    if "therapy_homework" not in st.session_state:
        st.session_state.therapy_homework = load_therapy_homework()


def load_therapy_sessions() -> List[Dict]:
    """Load therapy sessions from file."""
    try:
        if os.path.exists("data/therapy_sessions.json"):
            with open("data/therapy_sessions.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load therapy sessions: {e}")
    return []


def save_therapy_sessions(sessions: List[Dict]) -> bool:
    """Save therapy sessions to file."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/therapy_sessions.json", "w") as f:
            json.dump(sessions, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save therapy sessions: {e}")
        return False


def load_therapy_homework() -> List[Dict]:
    """Load therapy homework from file."""
    try:
        if os.path.exists("data/therapy_homework.json"):
            with open("data/therapy_homework.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load therapy homework: {e}")
    return []


def save_therapy_homework(homework: List[Dict]) -> bool:
    """Save therapy homework to file."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/therapy_homework.json", "w") as f:
            json.dump(homework, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save therapy homework: {e}")
        return False


def render_pre_session_prep():
    """Render pre-session preparation interface."""
    st.markdown("### 📋 Prepare for Your Next Session")
    st.info("""
    Take a few minutes before your therapy session to organize your thoughts. This helps you 
    make the most of your time with your therapist and ensures you don't forget important topics.
    """)
    
    # Session date
    col1, col2 = st.columns(2)
    with col1:
        session_date = st.date_input(
            "Upcoming Session Date:",
            value=datetime.now(),
            key="prep_session_date"
        )
    with col2:
        session_time = st.time_input(
            "Session Time:",
            value=datetime.now().time(),
            key="prep_session_time"
        )
    
    st.markdown("---")
    st.markdown("### 📝 Preparation Questions")
    st.caption("Reflect on these prompts to prepare for your session:")
    
    responses = {}
    
    for key, prompt_data in PREPARATION_PROMPTS.items():
        st.markdown(f"#### {prompt_data['icon']} {prompt_data['prompt']}")
        response = st.text_area(
            "",
            placeholder=prompt_data['help'],
            key=f"prep_{key}",
            height=100
        )
        responses[key] = response
    
    st.markdown("---")
    st.markdown("### ❓ Questions for My Therapist")
    st.caption("Write down any questions you want to ask during your session:")
    
    num_questions = st.number_input(
        "How many questions do you have?",
        min_value=0,
        max_value=10,
        value=1,
        key="num_questions"
    )
    
    questions = []
    for i in range(int(num_questions)):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            question = st.text_input(
                f"Question {i+1}:",
                key=f"question_{i}",
                placeholder="e.g., How can I manage anxiety in social situations?"
            )
        with col2:
            category = st.selectbox(
                "Category:",
                options=QUESTION_CATEGORIES,
                key=f"question_cat_{i}"
            )
        
        if question:
            questions.append({
                "question": question,
                "category": category
            })
    
    st.markdown("---")
    st.markdown("### 🎯 Main Topics to Discuss")
    st.caption("What are the most important things you want to talk about?")
    
    topics = st.text_area(
        "Priority topics for this session:",
        placeholder="e.g., Work stress, relationship with partner, sleep issues...",
        key="priority_topics",
        height=100
    )
    
    st.markdown("---")
    
    # Save preparation
    if st.button("💾 Save Session Preparation", use_container_width=True, type="primary"):
        prep_data = {
            "type": "preparation",
            "session_date": session_date.isoformat(),
            "session_time": session_time.isoformat(),
            "created_date": datetime.now().isoformat(),
            "responses": responses,
            "questions": questions,
            "topics": topics
        }
        
        st.session_state.therapy_sessions.append(prep_data)
        if save_therapy_sessions(st.session_state.therapy_sessions):
            st.success("✅ Session preparation saved! You're ready for your appointment.")
            st.info("💡 Tip: Review this before your session to refresh your memory.")


def render_post_session_notes():
    """Render post-session notes interface."""
    st.markdown("### 📝 Record Session Notes")
    st.info("""
    Right after your therapy session, capture the key insights, homework, and reflections 
    while they're fresh in your mind. These notes help you remember and apply what you learned.
    """)
    
    # Session details
    col1, col2, col3 = st.columns(3)
    with col1:
        session_date = st.date_input(
            "Session Date:",
            value=datetime.now(),
            key="post_session_date"
        )
    with col2:
        session_number = st.number_input(
            "Session #:",
            min_value=1,
            value=1,
            key="session_number"
        )
    with col3:
        session_rating = st.slider(
            "How helpful was this session?",
            min_value=1,
            max_value=10,
            value=7,
            key="session_rating"
        )
    
    st.markdown("---")
    st.markdown("### 💭 Session Reflections")
    
    reflections = {}
    
    for key, prompt_data in POST_SESSION_PROMPTS.items():
        st.markdown(f"#### {prompt_data['icon']} {prompt_data['prompt']}")
        reflection = st.text_area(
            "",
            placeholder=prompt_data['help'],
            key=f"post_{key}",
            height=100
        )
        reflections[key] = reflection
    
    st.markdown("---")
    st.markdown("### 📚 Techniques or Concepts Discussed")
    
    techniques = st.text_area(
        "What techniques, strategies, or concepts did you learn?",
        placeholder="e.g., Cognitive restructuring, breathing exercises, SMART goals...",
        key="techniques_learned",
        height=100
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Goals for Next Session")
    
    next_goals = st.text_area(
        "What do you want to work on or discuss next time?",
        placeholder="e.g., Practice new coping skills, discuss family relationships...",
        key="next_goals",
        height=100
    )
    
    st.markdown("---")
    
    # Save notes
    if st.button("💾 Save Session Notes", use_container_width=True, type="primary"):
        notes_data = {
            "type": "notes",
            "session_date": session_date.isoformat(),
            "session_number": int(session_number),
            "session_rating": session_rating,
            "created_date": datetime.now().isoformat(),
            "reflections": reflections,
            "techniques": techniques,
            "next_goals": next_goals
        }
        
        st.session_state.therapy_sessions.append(notes_data)
        if save_therapy_sessions(st.session_state.therapy_sessions):
            st.success("✅ Session notes saved!")
            
            # Check if there's homework to add
            if reflections.get("Homework assigned"):
                if st.button("➕ Add Homework Items"):
                    st.session_state.show_homework_add = True
                    st.rerun()


def render_homework_tracker():
    """Render therapy homework tracker."""
    st.markdown("### 📝 Therapy Homework Tracker")
    st.info("""
    Keep track of homework assignments from your therapist. Mark progress, set reminders, 
    and note your experiences with each task.
    """)
    
    # Add new homework
    with st.expander("➕ Add New Homework Assignment", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            homework_title = st.text_input(
                "Homework Title:",
                placeholder="e.g., Practice deep breathing daily",
                key="new_homework_title"
            )
            
            homework_description = st.text_area(
                "Description/Instructions:",
                placeholder="What did your therapist ask you to do?",
                key="new_homework_desc",
                height=100
            )
        
        with col2:
            assigned_date = st.date_input(
                "Assigned Date:",
                value=datetime.now(),
                key="homework_assigned_date"
            )
            
            due_date = st.date_input(
                "Due/Next Session Date:",
                value=datetime.now() + timedelta(days=7),
                key="homework_due_date"
            )
            
            frequency = st.text_input(
                "Frequency:",
                placeholder="e.g., Daily, 3x per week, As needed",
                key="homework_frequency"
            )
        
        if st.button("💾 Add Homework", key="add_homework_btn"):
            if homework_title:
                homework_item = {
                    "id": datetime.now().isoformat(),
                    "title": homework_title,
                    "description": homework_description,
                    "assigned_date": assigned_date.isoformat(),
                    "due_date": due_date.isoformat(),
                    "frequency": frequency,
                    "status": "Not Started",
                    "progress_notes": [],
                    "created_date": datetime.now().isoformat()
                }
                
                st.session_state.therapy_homework.append(homework_item)
                if save_therapy_homework(st.session_state.therapy_homework):
                    st.success("✅ Homework added!")
                    st.rerun()
            else:
                st.warning("Please enter a homework title.")
    
    # Display existing homework
    st.markdown("---")
    st.markdown("### 📋 Current Homework Assignments")
    
    if not st.session_state.therapy_homework:
        st.info("No homework assignments yet. Add one above to get started!")
        return
    
    # Filter options
    status_filter = st.multiselect(
        "Filter by status:",
        options=HOMEWORK_STATUS,
        default=["Not Started", "In Progress"],
        key="homework_status_filter"
    )
    
    # Display homework items
    filtered_homework = [
        hw for hw in st.session_state.therapy_homework
        if hw.get("status") in status_filter
    ]
    
    if not filtered_homework:
        st.info("No homework matches your filters.")
        return
    
    for i, hw in enumerate(filtered_homework):
        with st.expander(f"{'✅' if hw['status'] == 'Completed' else '📌'} {hw['title']}", expanded=False):
            col1, col2 = st.columns([0.7, 0.3])
            
            with col1:
                st.markdown(f"**Description:** {hw.get('description', 'N/A')}")
                st.caption(f"Frequency: {hw.get('frequency', 'Not specified')}")
                
                due_date = datetime.fromisoformat(hw['due_date']).date()
                days_until_due = (due_date - datetime.now().date()).days
                
                if days_until_due < 0:
                    st.error(f"⚠️ Overdue by {abs(days_until_due)} days")
                elif days_until_due == 0:
                    st.warning("📅 Due today!")
                else:
                    st.info(f"📅 Due in {days_until_due} days ({due_date.strftime('%b %d, %Y')})")
            
            with col2:
                new_status = st.selectbox(
                    "Status:",
                    options=HOMEWORK_STATUS,
                    index=HOMEWORK_STATUS.index(hw.get("status", "Not Started")),
                    key=f"hw_status_{i}"
                )
                
                if new_status != hw["status"]:
                    hw["status"] = new_status
                    save_therapy_homework(st.session_state.therapy_homework)
                    st.success("Status updated!")
            
            # Progress notes
            st.markdown("**Progress Notes:**")
            progress_notes = hw.get("progress_notes", [])
            
            if progress_notes:
                for note in progress_notes[-3:]:  # Show last 3 notes
                    note_date = datetime.fromisoformat(note['date']).strftime("%b %d, %Y")
                    st.caption(f"*{note_date}:* {note['note']}")
            
            new_note = st.text_input(
                "Add progress note:",
                key=f"hw_note_{i}",
                placeholder="How did it go? Any challenges or insights?"
            )
            
            if st.button("➕ Add Note", key=f"hw_add_note_{i}"):
                if new_note:
                    hw.setdefault("progress_notes", []).append({
                        "date": datetime.now().isoformat(),
                        "note": new_note
                    })
                    save_therapy_homework(st.session_state.therapy_homework)
                    st.success("Note added!")
                    st.rerun()


def render_session_timeline():
    """Render timeline of therapy sessions."""
    st.markdown("### 📅 Session Timeline")
    
    if not st.session_state.therapy_sessions:
        st.info("No sessions recorded yet. Start by preparing for a session or recording session notes!")
        return
    
    st.info("""
    View your therapy journey over time. Track your progress, review past insights, 
    and see how far you've come.
    """)
    
    # Sort sessions by date
    sorted_sessions = sorted(
        st.session_state.therapy_sessions,
        key=lambda x: x.get('session_date', x.get('created_date')),
        reverse=True
    )
    
    # Statistics
    total_sessions = len([s for s in sorted_sessions if s.get('type') == 'notes'])
    preparations = len([s for s in sorted_sessions if s.get('type') == 'preparation'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sessions", total_sessions)
    with col2:
        st.metric("Preparations", preparations)
    with col3:
        if total_sessions > 0:
            notes_sessions = [s for s in sorted_sessions if s.get('type') == 'notes' and s.get('session_rating')]
            if notes_sessions:
                avg_rating = sum(s['session_rating'] for s in notes_sessions) / len(notes_sessions)
                st.metric("Avg. Rating", f"{avg_rating:.1f}/10")
    
    st.markdown("---")
    
    # Display sessions
    for session in sorted_sessions:
        session_date = datetime.fromisoformat(session.get('session_date', session.get('created_date')))
        date_str = session_date.strftime("%B %d, %Y")
        
        if session['type'] == 'preparation':
            icon = "📋"
            title = f"Pre-Session Preparation - {date_str}"
        else:
            icon = "📝"
            session_num = session.get('session_number', '?')
            rating = session.get('session_rating', 0)
            stars = "⭐" * rating
            title = f"Session #{session_num} - {date_str} {stars}"
        
        with st.expander(f"{icon} {title}"):
            if session['type'] == 'preparation':
                st.markdown("**Preparation Responses:**")
                for key, response in session.get('responses', {}).items():
                    if response:
                        prompt_info = PREPARATION_PROMPTS.get(key, {})
                        st.markdown(f"**{prompt_info.get('icon', '•')} {prompt_info.get('prompt', key)}:**")
                        st.write(response)
                        st.markdown("---")
                
                if session.get('questions'):
                    st.markdown("**Questions to Ask:**")
                    for q in session['questions']:
                        st.write(f"• {q['question']} *({q['category']})*")
                
                if session.get('topics'):
                    st.markdown("**Priority Topics:**")
                    st.write(session['topics'])
            
            else:  # notes
                st.markdown(f"**Session Rating:** {session.get('session_rating', 'N/A')}/10")
                st.markdown("---")
                
                st.markdown("**Session Reflections:**")
                for key, reflection in session.get('reflections', {}).items():
                    if reflection:
                        prompt_info = POST_SESSION_PROMPTS.get(key, {})
                        st.markdown(f"**{prompt_info.get('icon', '•')} {prompt_info.get('prompt', key)}:**")
                        st.write(reflection)
                        st.markdown("---")
                
                if session.get('techniques'):
                    st.markdown("**Techniques/Concepts Learned:**")
                    st.write(session['techniques'])
                    st.markdown("---")
                
                if session.get('next_goals'):
                    st.markdown("**Goals for Next Session:**")
                    st.write(session['next_goals'])


def render_export_summary():
    """Render export functionality for session summaries."""
    st.markdown("### 📤 Export Session Summary")
    st.info("""
    Create a summary of your therapy journey to share with your therapist or for your own records. 
    Choose what information to include.
    """)
    
    if not st.session_state.therapy_sessions:
        st.warning("No sessions to export yet.")
        return
    
    # Export options
    st.markdown("**Select what to include:**")
    
    col1, col2 = st.columns(2)
    with col1:
        include_prep = st.checkbox("Pre-session preparations", value=True, key="export_prep")
        include_notes = st.checkbox("Session notes", value=True, key="export_notes")
        include_homework = st.checkbox("Homework assignments", value=True, key="export_homework")
    
    with col2:
        date_range = st.selectbox(
            "Time period:",
            options=["Last session", "Last 3 sessions", "Last month", "Last 3 months", "All time"],
            key="export_date_range"
        )
    
    # Generate summary
    if st.button("📄 Generate Summary", use_container_width=True, type="primary"):
        summary_text = "# Therapy Session Summary\n\n"
        summary_text += f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n"
        summary_text += "---\n\n"
        
        # Filter sessions based on date range
        if date_range == "Last session":
            sessions_to_export = st.session_state.therapy_sessions[-1:]
        elif date_range == "Last 3 sessions":
            sessions_to_export = st.session_state.therapy_sessions[-3:]
        elif date_range == "Last month":
            cutoff = datetime.now() - timedelta(days=30)
            sessions_to_export = [
                s for s in st.session_state.therapy_sessions
                if datetime.fromisoformat(s.get('session_date', s.get('created_date'))) >= cutoff
            ]
        elif date_range == "Last 3 months":
            cutoff = datetime.now() - timedelta(days=90)
            sessions_to_export = [
                s for s in st.session_state.therapy_sessions
                if datetime.fromisoformat(s.get('session_date', s.get('created_date'))) >= cutoff
            ]
        else:  # All time
            sessions_to_export = st.session_state.therapy_sessions
        
        # Add sessions to summary
        for session in sessions_to_export:
            session_date = datetime.fromisoformat(session.get('session_date', session.get('created_date')))
            date_str = session_date.strftime("%B %d, %Y")
            
            if session['type'] == 'preparation' and include_prep:
                summary_text += f"## Pre-Session Preparation - {date_str}\n\n"
                for key, response in session.get('responses', {}).items():
                    if response:
                        prompt_info = PREPARATION_PROMPTS.get(key, {})
                        summary_text += f"**{prompt_info.get('prompt', key)}:**\n{response}\n\n"
                
                if session.get('topics'):
                    summary_text += f"**Priority Topics:**\n{session['topics']}\n\n"
                
                summary_text += "---\n\n"
            
            elif session['type'] == 'notes' and include_notes:
                session_num = session.get('session_number', '?')
                rating = session.get('session_rating', 'N/A')
                summary_text += f"## Session #{session_num} - {date_str}\n\n"
                summary_text += f"**Rating:** {rating}/10\n\n"
                
                for key, reflection in session.get('reflections', {}).items():
                    if reflection:
                        prompt_info = POST_SESSION_PROMPTS.get(key, {})
                        summary_text += f"**{prompt_info.get('prompt', key)}:**\n{reflection}\n\n"
                
                if session.get('techniques'):
                    summary_text += f"**Techniques/Concepts:**\n{session['techniques']}\n\n"
                
                summary_text += "---\n\n"
        
        # Add homework if requested
        if include_homework and st.session_state.therapy_homework:
            summary_text += "## Therapy Homework\n\n"
            for hw in st.session_state.therapy_homework:
                summary_text += f"### {hw['title']}\n"
                summary_text += f"**Status:** {hw.get('status', 'N/A')}\n"
                summary_text += f"**Description:** {hw.get('description', 'N/A')}\n"
                if hw.get('progress_notes'):
                    summary_text += "**Progress Notes:**\n"
                    for note in hw['progress_notes']:
                        note_date = datetime.fromisoformat(note['date']).strftime('%b %d, %Y')
                        summary_text += f"- {note_date}: {note['note']}\n"
                summary_text += "\n"
        
        # Display summary
        st.markdown("---")
        st.markdown("### 📄 Your Summary")
        st.text_area(
            "Copy this text to share with your therapist:",
            value=summary_text,
            height=400,
            key="summary_output"
        )
        
        st.download_button(
            label="💾 Download as Text File",
            data=summary_text,
            file_name=f"therapy_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )


def render_tips_guide():
    """Render tips for maximizing therapy effectiveness."""
    st.markdown("### 💡 Maximizing Your Therapy Sessions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Before Your Session:")
        st.success("""
        • **Review your week:** Use the preparation prompts
        • **List priorities:** What's most important to discuss?
        • **Write questions:** Don't rely on memory
        • **Check homework:** Review progress on assignments
        • **Set intention:** What do you hope to gain?
        • **Arrive early:** Give yourself time to settle
        • **Be honest:** Prepare to be vulnerable
        """)
        
        st.markdown("#### 💭 During Your Session:")
        st.info("""
        • **Be present:** Put phone away, focus fully
        • **Be honest:** Share openly, even if difficult
        • **Ask questions:** If confused, speak up
        • **Take notes:** Jot down key insights
        • **Provide feedback:** Let therapist know what's helpful
        • **Stay engaged:** Participate actively
        • **Request clarification:** Make sure you understand
        """)
    
    with col2:
        st.markdown("#### 📝 After Your Session:")
        st.warning("""
        • **Record notes:** Capture insights while fresh
        • **Write homework:** Document assignments clearly
        • **Reflect:** How are you feeling?
        • **Plan actions:** What will you do this week?
        • **Practice skills:** Use what you learned
        • **Be patient:** Change takes time
        • **Schedule next:** Book your next appointment
        """)
        
        st.markdown("#### 🎯 Between Sessions:")
        st.success("""
        • **Do homework:** Practice assigned skills
        • **Track progress:** Notice changes and patterns
        • **Use tools:** Apply coping strategies learned
        • **Journal:** Write about experiences
        • **Be compassionate:** Progress isn't linear
        • **Prepare ahead:** Start thinking about next session
        • **Reach out:** Contact therapist if crisis
        """)
    
    st.markdown("---")
    st.markdown("### ❓ Common Therapy Challenges")
    
    st.info("""
    **"I forget everything once I'm in the room"**
    - Solution: Use the preparation tool! Bring written notes to reference.
    
    **"I don't know what to talk about"**
    - Solution: Review your week with the prompts. Any emotion, event, or pattern is valid.
    
    **"I feel like I'm wasting time with small talk"**
    - Solution: Jump right in! Say "I want to talk about [specific issue]."
    
    **"I don't feel comfortable being vulnerable"**
    - Solution: Tell your therapist this! It's okay to go slow and build trust.
    
    **"I'm not seeing progress"**
    - Solution: Review your session notes over time. Progress can be subtle. Discuss with therapist.
    
    **"I don't understand the homework"**
    - Solution: Ask for clarification! Email or call your therapist between sessions.
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Making Therapy Work for You")
    
    st.markdown("""
    **Remember:**
    - Therapy is YOUR time and YOUR investment
    - You're the expert on your own experience
    - It's okay to disagree with your therapist
    - You can change therapists if it's not a good fit
    - Progress isn't always linear - setbacks are normal
    - The work happens between sessions, not just during
    - You deserve support and healing
    
    **Red flags (consider finding a new therapist if they):**
    - Break confidentiality without cause
    - Are judgmental or dismissive
    - Push their personal beliefs
    - Create inappropriate boundaries
    - Make you feel worse consistently
    - Don't tailor approach to you
    """)


def render_therapy_tool():
    """Main render function for therapy preparation tool."""
    st.header("📈 Therapy Preparation & Session Notes")
    
    # Initialize state
    initialize_therapy_state()
    
    st.info("""
    💼 Maximize the effectiveness of your therapy! Prepare for sessions, track homework, 
    record insights, and review your progress over time. Many people forget important topics 
    or insights - this tool helps you bridge the gap between sessions.
    """)
    
    # Tab navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Pre-Session Prep",
        "📝 Session Notes",
        "✅ Homework Tracker",
        "📅 Timeline",
        "📤 Export",
        "💡 Tips"
    ])
    
    with tab1:
        st.markdown("""
        Prepare for your upcoming therapy session. Organize your thoughts, list questions, 
        and identify priorities to discuss.
        """)
        render_pre_session_prep()
    
    with tab2:
        st.markdown("""
        Record notes immediately after your session. Capture key insights, homework assignments, 
        and reflections while they're fresh.
        """)
        render_post_session_notes()
    
    with tab3:
        st.markdown("""
        Track homework assignments from your therapist. Mark progress, add notes, and 
        stay on top of your therapeutic work.
        """)
        render_homework_tracker()
    
    with tab4:
        st.markdown("""
        View your complete therapy journey. Review past sessions, see your progress, 
        and reflect on how far you've come.
        """)
        render_session_timeline()
    
    with tab5:
        st.markdown("""
        Export a summary of your therapy sessions to share with your therapist or 
        keep for your records.
        """)
        render_export_summary()
    
    with tab6:
        render_tips_guide()
    
    # Quick reminder at bottom
    st.markdown("---")
    st.success("""
    💡 **Remember:** Therapy is most effective when you actively engage between sessions. 
    Use this tool to stay connected to your therapeutic work!
    """)
