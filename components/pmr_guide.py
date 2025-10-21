"""
Progressive Muscle Relaxation (PMR) Guide Component
Interactive, step-by-step guided progressive muscle relaxation exercise.
Walks users through tensing and relaxing different muscle groups with timing cues
and optional audio guidance.
"""

import streamlit as st
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
import time as time_module

# Muscle groups for PMR (in order)
MUSCLE_GROUPS = [
    {
        "name": "Feet",
        "icon": "🦶",
        "tense_instruction": "Curl your toes downward and tense your feet",
        "relax_instruction": "Release and let your feet completely relax",
        "visualization": "Feel the tension melting away from your feet",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Calves",
        "icon": "🦵",
        "tense_instruction": "Point your toes upward and tense your calf muscles",
        "relax_instruction": "Release the tension and feel your calves soften",
        "visualization": "Notice the difference between tension and relaxation",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Thighs",
        "icon": "🦵",
        "tense_instruction": "Squeeze your thigh muscles tightly",
        "relax_instruction": "Let go and feel your thighs become heavy and relaxed",
        "visualization": "Imagine warmth flowing through your legs",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Buttocks",
        "icon": "💺",
        "tense_instruction": "Tighten your buttock muscles",
        "relax_instruction": "Release completely and sink into your seat",
        "visualization": "Feel yourself becoming more grounded and stable",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Abdomen",
        "icon": "🫃",
        "tense_instruction": "Tighten your stomach muscles, pulling them in",
        "relax_instruction": "Let your belly soften and relax completely",
        "visualization": "Allow your breath to flow naturally and easily",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Chest",
        "icon": "🫁",
        "tense_instruction": "Take a deep breath and tighten your chest muscles",
        "relax_instruction": "Exhale and release all tension from your chest",
        "visualization": "Feel your breathing become easier and deeper",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Back",
        "icon": "🔙",
        "tense_instruction": "Arch your back slightly and tense the muscles",
        "relax_instruction": "Release and let your back sink into support",
        "visualization": "Imagine tension draining from your spine",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Hands",
        "icon": "✊",
        "tense_instruction": "Make tight fists with both hands",
        "relax_instruction": "Open your hands and let your fingers relax",
        "visualization": "Notice the warmth in your palms and fingers",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Arms",
        "icon": "💪",
        "tense_instruction": "Tense your biceps and forearms",
        "relax_instruction": "Let your arms hang loosely and feel heavy",
        "visualization": "Feel the relaxation spreading through your arms",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Shoulders",
        "icon": "🤷",
        "tense_instruction": "Raise your shoulders up toward your ears",
        "relax_instruction": "Drop your shoulders down and feel the release",
        "visualization": "Imagine stress melting off your shoulders",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Neck",
        "icon": "🧣",
        "tense_instruction": "Gently press your head back and tense your neck",
        "relax_instruction": "Return to center and let your neck relax",
        "visualization": "Feel your neck becoming loose and comfortable",
        "tense_duration": 5,
        "relax_duration": 10
    },
    {
        "name": "Face & Jaw",
        "icon": "😌",
        "tense_instruction": "Scrunch up your facial muscles and clench your jaw",
        "relax_instruction": "Release all tension, letting your jaw drop slightly",
        "visualization": "Feel your face becoming smooth and peaceful",
        "tense_duration": 5,
        "relax_duration": 10
    }
]

# Session durations
SESSION_DURATIONS = {
    "Quick (5 minutes)": {
        "duration": 5,
        "groups": [0, 4, 8, 9, 11],  # Feet, Abdomen, Hands, Shoulders, Face
        "description": "Essential muscle groups for quick relief"
    },
    "Standard (10 minutes)": {
        "duration": 10,
        "groups": [0, 2, 4, 6, 8, 9, 11],  # Feet, Thighs, Abdomen, Back, Hands, Shoulders, Face
        "description": "Balanced routine covering major areas"
    },
    "Full Body (20 minutes)": {
        "duration": 20,
        "groups": list(range(12)),  # All muscle groups
        "description": "Complete progressive muscle relaxation"
    }
}

# Background sounds for PMR
PMR_SOUNDS = [
    "None (Silent)",
    "ocean_waves.wav",
    "rain_sounds.wav",
    "forest_ambience.wav",
    "tibetan_bowls.wav",
    "silent_soft_music.wav"
]


def initialize_pmr_state():
    """Initialize session state for PMR."""
    if "pmr_history" not in st.session_state:
        st.session_state.pmr_history = load_pmr_history()
    if "pmr_active" not in st.session_state:
        st.session_state.pmr_active = False
    if "pmr_current_group" not in st.session_state:
        st.session_state.pmr_current_group = 0
    if "pmr_phase" not in st.session_state:
        st.session_state.pmr_phase = "prepare"  # prepare, tense, relax, complete
    if "pmr_start_time" not in st.session_state:
        st.session_state.pmr_start_time = None


def load_pmr_history() -> List[Dict]:
    """Load PMR history from file."""
    try:
        if os.path.exists("data/pmr_history.json"):
            with open("data/pmr_history.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load PMR history: {e}")
    return []


def save_pmr_history(history: List[Dict]) -> bool:
    """Save PMR history to file."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/pmr_history.json", "w") as f:
            json.dump(history, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save PMR history: {e}")
        return False


def log_pmr_session(duration_type: str, muscle_groups_completed: int, rating: int = 0):
    """Log a completed PMR session."""
    entry = {
        "date": datetime.now().isoformat(),
        "duration_type": duration_type,
        "muscle_groups": muscle_groups_completed,
        "rating": rating,
        "completed": True,
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.pmr_history.append(entry)
    save_pmr_history(st.session_state.pmr_history)


def render_muscle_group_visual(group: Dict, phase: str):
    """Render visual representation of current muscle group."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Large icon
        st.markdown(f"""
        <div style='text-align: center; font-size: 120px; padding: 20px;'>
            {group['icon']}
        </div>
        """, unsafe_allow_html=True)
        
        # Muscle group name
        st.markdown(f"""
        <div style='text-align: center; font-size: 36px; font-weight: bold; color: #4A90E2;'>
            {group['name']}
        </div>
        """, unsafe_allow_html=True)


def render_guided_session():
    """Render the guided PMR session."""
    st.markdown("### 🧘‍♀️ Guided Progressive Muscle Relaxation")
    
    # Session setup
    if not st.session_state.pmr_active:
        st.info("""
        Find a comfortable position (sitting or lying down) where you won't be disturbed. 
        You'll be guided through tensing and relaxing different muscle groups.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            session_type = st.selectbox(
                "Session Duration:",
                options=list(SESSION_DURATIONS.keys()),
                key="pmr_session_type"
            )
            
            session_info = SESSION_DURATIONS[session_type]
            st.caption(f"⏱️ {session_info['duration']} minutes")
            st.caption(f"📍 {session_info['description']}")
        
        with col2:
            background_sound = st.selectbox(
                "Background Sound:",
                options=PMR_SOUNDS,
                key="pmr_background_sound"
            )
            
            if background_sound != "None (Silent)":
                st.caption("🔊 Calming background audio will play")
        
        st.markdown("---")
        
        # Instructions
        with st.expander("📖 How Progressive Muscle Relaxation Works"):
            st.markdown("""
            **PMR involves two steps for each muscle group:**
            
            1. **Tense:** Contract the muscle group for 5 seconds
            2. **Relax:** Release the tension and relax for 10 seconds
            
            **Tips for success:**
            - Focus on the contrast between tension and relaxation
            - Breathe naturally throughout
            - Don't tense to the point of pain - moderate tension is enough
            - If you have an injury, skip that muscle group
            - Take your time and enjoy the process
            """)
        
        # Start button
        if st.button("▶️ Start Session", use_container_width=True, type="primary"):
            st.session_state.pmr_active = True
            st.session_state.pmr_current_group = 0
            st.session_state.pmr_phase = "prepare"
            st.session_state.pmr_start_time = datetime.now()
            st.session_state.pmr_session_type = session_type
            st.session_state.pmr_groups_to_do = session_info['groups']
            st.rerun()
    
    else:
        # Active session
        session_info = SESSION_DURATIONS[st.session_state.pmr_session_type]
        groups_to_do = st.session_state.pmr_groups_to_do
        
        # Check if session is complete
        if st.session_state.pmr_current_group >= len(groups_to_do):
            st.success("🎉 Congratulations! You've completed the PMR session!")
            st.balloons()
            
            # Session summary
            elapsed = datetime.now() - st.session_state.pmr_start_time
            elapsed_minutes = int(elapsed.total_seconds() / 60)
            
            st.markdown(f"""
            **Session Summary:**
            - Duration: {elapsed_minutes} minutes
            - Muscle groups: {len(groups_to_do)}
            - Type: {st.session_state.pmr_session_type}
            """)
            
            # Rating
            rating = st.slider(
                "How relaxed do you feel? (1 = Not at all, 10 = Very relaxed)",
                min_value=1,
                max_value=10,
                value=7,
                key="pmr_rating"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save & Finish", use_container_width=True):
                    log_pmr_session(
                        st.session_state.pmr_session_type,
                        len(groups_to_do),
                        rating
                    )
                    st.session_state.pmr_active = False
                    st.success("Session saved!")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Start New Session", use_container_width=True):
                    st.session_state.pmr_active = False
                    st.session_state.pmr_current_group = 0
                    st.rerun()
            
            return
        
        # Get current muscle group
        current_group_index = groups_to_do[st.session_state.pmr_current_group]
        current_group = MUSCLE_GROUPS[current_group_index]
        
        # Progress indicator
        progress = st.session_state.pmr_current_group / len(groups_to_do)
        st.progress(progress)
        st.caption(f"Muscle group {st.session_state.pmr_current_group + 1} of {len(groups_to_do)}")
        
        # Visual representation
        render_muscle_group_visual(current_group, st.session_state.pmr_phase)
        
        st.markdown("---")
        
        # Phase-specific instructions
        if st.session_state.pmr_phase == "prepare":
            st.info(f"**Prepare:** Focus on your {current_group['name'].lower()}")
            st.markdown(f"Get ready to tense this muscle group...")
            
            if st.button("Ready ▶️", use_container_width=True, type="primary"):
                st.session_state.pmr_phase = "tense"
                st.rerun()
        
        elif st.session_state.pmr_phase == "tense":
            st.warning(f"**Tense:** {current_group['tense_instruction']}")
            st.markdown("Hold for 5 seconds... Feel the tension...")
            
            # Countdown could be added here
            if st.button("Release ▶️", use_container_width=True, type="primary"):
                st.session_state.pmr_phase = "relax"
                st.rerun()
        
        elif st.session_state.pmr_phase == "relax":
            st.success(f"**Relax:** {current_group['relax_instruction']}")
            st.markdown(f"*{current_group['visualization']}*")
            st.markdown("Take 10 seconds to notice the difference...")
            
            if st.button("Next ▶️", use_container_width=True, type="primary"):
                st.session_state.pmr_current_group += 1
                st.session_state.pmr_phase = "prepare"
                st.rerun()
        
        # Play background sound if selected
        if st.session_state.get('pmr_background_sound') and st.session_state.pmr_background_sound != "None (Silent)":
            try:
                st.audio(f"audio_files/{st.session_state.pmr_background_sound}", format="audio/wav")
            except:
                pass
        
        # Exit button
        st.markdown("---")
        if st.button("⏹️ End Session Early"):
            st.session_state.pmr_active = False
            st.rerun()


def render_muscle_group_library():
    """Render library of all muscle groups with instructions."""
    st.markdown("### 📚 Muscle Group Library")
    st.info("Browse all muscle groups and their PMR instructions. Use this as a reference or for targeted relaxation.")
    
    for i, group in enumerate(MUSCLE_GROUPS, 1):
        with st.expander(f"{group['icon']} {i}. {group['name']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Tensing:**")
                st.info(group['tense_instruction'])
                st.caption(f"Duration: {group['tense_duration']} seconds")
            
            with col2:
                st.markdown("**Relaxing:**")
                st.success(group['relax_instruction'])
                st.caption(f"Duration: {group['relax_duration']} seconds")
            
            st.markdown("**Visualization:**")
            st.markdown(f"*{group['visualization']}*")


def render_session_history():
    """Render PMR session history and statistics."""
    st.markdown("### 📊 Session History & Statistics")
    
    if not st.session_state.pmr_history:
        st.info("No PMR sessions recorded yet. Complete a session to start tracking!")
        return
    
    # Statistics
    total_sessions = len(st.session_state.pmr_history)
    avg_rating = sum(s.get('rating', 0) for s in st.session_state.pmr_history) / total_sessions if total_sessions > 0 else 0
    
    # Count by duration type
    duration_counts = {}
    for session in st.session_state.pmr_history:
        dtype = session.get('duration_type', 'Unknown')
        duration_counts[dtype] = duration_counts.get(dtype, 0) + 1
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sessions", total_sessions)
    with col2:
        st.metric("Average Relaxation", f"{avg_rating:.1f}/10")
    with col3:
        most_used = max(duration_counts.items(), key=lambda x: x[1])[0] if duration_counts else "N/A"
        st.metric("Most Used", most_used.split()[0])
    
    # Recent sessions
    st.markdown("---")
    st.markdown("### 📅 Recent Sessions")
    
    recent = sorted(
        st.session_state.pmr_history,
        key=lambda x: x['date'],
        reverse=True
    )[:10]
    
    for session in recent:
        date_str = datetime.fromisoformat(session['date']).strftime("%B %d, %Y at %I:%M %p")
        with st.expander(f"🧘‍♀️ {session.get('duration_type', 'Unknown')} - {date_str}"):
            st.write(f"**Muscle groups completed:** {session.get('muscle_groups', 0)}")
            st.write(f"**Relaxation rating:** {session.get('rating', 0)}/10")
            if session.get('rating', 0) >= 8:
                st.success("High relaxation achieved! ✨")


def render_education():
    """Render educational content about PMR."""
    st.markdown("### 📚 About Progressive Muscle Relaxation")
    
    st.info("""
    **Progressive Muscle Relaxation (PMR)** is a deep relaxation technique developed by 
    Dr. Edmund Jacobson in the 1930s. It's based on the principle that mental calmness is 
    a natural result of physical relaxation.
    """)
    
    st.markdown("---")
    st.markdown("### 🔬 How PMR Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**The Science:**")
        st.success("""
        • **Physical tension → Mental stress** are connected
        • Tensing then releasing teaches body to recognize relaxation
        • Activates parasympathetic nervous system (rest & digest)
        • Reduces cortisol (stress hormone)
        • Improves body awareness
        • Creates mind-body connection
        """)
    
    with col2:
        st.markdown("**Benefits of PMR:**")
        st.info("""
        • Reduces physical tension and pain
        • Decreases anxiety and stress
        • Improves sleep quality
        • Lowers blood pressure
        • Helps with headaches and migraines
        • Reduces panic attack symptoms
        • Complements other therapies
        • Easy to learn and practice anywhere
        """)
    
    st.markdown("---")
    st.markdown("### 💡 When to Use PMR")
    
    st.markdown("""
    **Best times for practice:**
    - When feeling physically tense or stressed
    - Before bed to improve sleep
    - During anxiety or panic episodes
    - After stressful events
    - As a daily relaxation routine
    - When traditional meditation feels difficult
    
    **Who benefits most:**
    - People with anxiety disorders
    - Those with chronic pain or tension
    - Individuals who struggle with sitting meditation
    - Anyone with stress-related symptoms
    - People with insomnia
    - Those recovering from trauma (with guidance)
    """)
    
    st.markdown("---")
    st.markdown("### ⚠️ Important Notes")
    
    st.warning("""
    **Safety considerations:**
    - Don't tense to the point of pain
    - Skip muscle groups with injuries
    - Consult doctor if you have muscle/joint conditions
    - Be gentle with neck and back
    - Stop if you experience pain
    - Pregnant women should consult healthcare provider
    
    **Tips for beginners:**
    - Start with shorter sessions (5 minutes)
    - Practice in a quiet, comfortable space
    - Be patient - it gets easier with practice
    - Consistency matters more than duration
    - Can be done sitting or lying down
    - No special equipment needed
    """)
    
    st.markdown("---")
    st.markdown("### 📖 Additional Resources")
    
    st.markdown("""
    **Books:**
    - "The Relaxation and Stress Reduction Workbook" by Martha Davis
    - "Progressive Relaxation" by Edmund Jacobson (original)
    - "Full Catastrophe Living" by Jon Kabat-Zinn (includes PMR)
    
    **Research:**
    - 70+ years of scientific study support PMR's effectiveness
    - Shown to reduce anxiety in clinical trials
    - Effective for both physical and psychological tension
    - Often taught in therapy and medical settings
    
    **Integration with other practices:**
    - Combine with deep breathing for enhanced effect
    - Use before meditation to prepare body
    - Practice after yoga or exercise
    - Part of comprehensive anxiety treatment
    """)


def render_pmr_guide():
    """Main render function for Progressive Muscle Relaxation Guide."""
    st.header("🧩 Progressive Muscle Relaxation Guide")
    
    # Initialize state
    initialize_pmr_state()
    
    st.info("""
    💆‍♀️ Progressive Muscle Relaxation (PMR) is a proven technique for reducing physical tension 
    and anxiety. By systematically tensing and relaxing muscle groups, you'll learn to recognize 
    and release tension in your body.
    """)
    
    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧘‍♀️ Guided Session",
        "📚 Muscle Groups",
        "📊 History",
        "ℹ️ Learn About PMR"
    ])
    
    with tab1:
        st.markdown("""
        Follow the guided session to practice Progressive Muscle Relaxation. Choose your duration 
        and let the tool walk you through each muscle group.
        """)
        render_guided_session()
    
    with tab2:
        st.markdown("""
        Reference library of all muscle groups with tensing and relaxing instructions. 
        Use this to learn the technique or practice specific areas.
        """)
        render_muscle_group_library()
    
    with tab3:
        st.markdown("""
        Track your PMR practice over time. See how often you practice and how relaxed you feel.
        """)
        render_session_history()
    
    with tab4:
        render_education()
    
    # Quick tip at bottom
    st.markdown("---")
    st.success("""
    💡 **Quick Tip:** For best results, practice PMR regularly (daily if possible). 
    Even 5 minutes can make a difference in reducing tension and anxiety!
    """)
