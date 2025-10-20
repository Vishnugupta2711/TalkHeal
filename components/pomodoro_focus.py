"""
Pomodoro Focus Technique with Mindful Breaks Component
Enhanced focus session tool using the Pomodoro Technique (25 min work + 5 min break cycles).
During breaks, suggests and guides micro-wellness activities for restorative rest.
Tracks completed pomodoros and productivity patterns.
"""

import streamlit as st
from datetime import datetime, timedelta, time
import json
import os
from typing import Dict, List, Optional
import time as time_module

# Pomodoro session types
SESSION_TYPES = {
    "Pomodoro (25 min)": 25,
    "Short Pomodoro (15 min)": 15,
    "Long Pomodoro (45 min)": 45,
    "Custom Duration": 0
}

# Break durations
BREAK_TYPES = {
    "Short Break (5 min)": 5,
    "Long Break (15 min)": 15,
    "Custom Break": 0
}

# Mindful break activities
MINDFUL_BREAK_ACTIVITIES = {
    "Deep Breathing": {
        "icon": "🌬️",
        "duration": "1-2 minutes",
        "instructions": [
            "Sit comfortably and close your eyes",
            "Breathe in slowly through your nose for 4 counts",
            "Hold your breath for 4 counts",
            "Exhale slowly through your mouth for 6 counts",
            "Repeat 5-10 times",
            "Notice how you feel calmer and more centered"
        ],
        "benefits": "Reduces stress, lowers heart rate, improves focus"
    },
    "Desk Stretches": {
        "icon": "🤸",
        "duration": "2-3 minutes",
        "instructions": [
            "Stand up from your desk",
            "Stretch arms overhead and reach for the ceiling",
            "Roll your shoulders backwards 5 times",
            "Tilt your head gently side to side",
            "Twist your torso left and right",
            "Shake out your hands and arms",
            "Take a few steps if possible"
        ],
        "benefits": "Releases tension, improves circulation, reduces physical strain"
    },
    "Gratitude Reflection": {
        "icon": "🙏",
        "duration": "1-2 minutes",
        "instructions": [
            "Think of three things you're grateful for right now",
            "They can be big or small",
            "Take a moment to truly appreciate each one",
            "Notice the positive feelings that arise",
            "Smile and carry this feeling forward"
        ],
        "benefits": "Boosts mood, increases positive emotions, improves mental health"
    },
    "Window Gazing / Nature": {
        "icon": "🪟",
        "duration": "2-3 minutes",
        "instructions": [
            "Look out a window or step outside if possible",
            "Focus on something in nature (tree, sky, clouds, birds)",
            "Let your eyes relax and soften",
            "Notice details you normally overlook",
            "Take a few deep breaths while observing",
            "Allow your mind to rest"
        ],
        "benefits": "Reduces eye strain, mental refresh, connects with nature"
    },
    "Mindful Walking": {
        "icon": "🚶",
        "duration": "3-5 minutes",
        "instructions": [
            "Walk slowly and deliberately",
            "Notice the sensation of your feet touching the ground",
            "Feel your body moving through space",
            "Observe your surroundings without judgment",
            "Breathe naturally and stay present",
            "Return feeling refreshed"
        ],
        "benefits": "Physical movement, mental clarity, mindfulness practice"
    },
    "Water & Hydration": {
        "icon": "💧",
        "duration": "1 minute",
        "instructions": [
            "Get a glass of water",
            "Drink it slowly and mindfully",
            "Notice the temperature and sensation",
            "Feel the water refreshing your body",
            "Take a moment to appreciate hydration",
            "Refill your water bottle for later"
        ],
        "benefits": "Hydration, mental clarity, physical refresh"
    },
    "Eye Rest (20-20-20 Rule)": {
        "icon": "👀",
        "duration": "1 minute",
        "instructions": [
            "Look away from your screen",
            "Focus on something 20 feet away",
            "Keep your gaze there for 20 seconds",
            "Blink several times",
            "Close your eyes for a few seconds",
            "Repeat if needed"
        ],
        "benefits": "Reduces eye strain, prevents digital eye fatigue"
    },
    "Positive Affirmation": {
        "icon": "✨",
        "duration": "1 minute",
        "instructions": [
            "Choose an affirmation that resonates with you",
            "Examples: 'I am capable and strong', 'I am doing my best'",
            "Repeat it slowly 3-5 times",
            "Say it with conviction and belief",
            "Notice any positive feelings that arise",
            "Carry this energy into your next session"
        ],
        "benefits": "Boosts confidence, positive self-talk, motivation"
    }
}

# Focus music/sounds (referencing existing audio files)
FOCUS_SOUNDS = [
    "None (Silent)",
    "forest_ambience.wav",
    "gentle_piano.wav",
    "ocean_waves.wav",
    "rain_sounds.wav",
    "silent_soft_music.wav",
    "tibetan_bowls.wav"
]


def initialize_pomodoro_state():
    """Initialize session state for pomodoro timer."""
    if "pomodoro_history" not in st.session_state:
        st.session_state.pomodoro_history = load_pomodoro_history()
    if "pomodoro_active" not in st.session_state:
        st.session_state.pomodoro_active = False
    if "pomodoro_start_time" not in st.session_state:
        st.session_state.pomodoro_start_time = None
    if "pomodoro_duration" not in st.session_state:
        st.session_state.pomodoro_duration = 25
    if "pomodoro_type" not in st.session_state:
        st.session_state.pomodoro_type = "work"
    if "pomodoros_completed_today" not in st.session_state:
        st.session_state.pomodoros_completed_today = 0
    if "break_activity" not in st.session_state:
        st.session_state.break_activity = None


def load_pomodoro_history() -> List[Dict]:
    """Load pomodoro history from file."""
    try:
        if os.path.exists("data/pomodoro_history.json"):
            with open("data/pomodoro_history.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load pomodoro history: {e}")
    return []


def save_pomodoro_history(history: List[Dict]) -> bool:
    """Save pomodoro history to file."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/pomodoro_history.json", "w") as f:
            json.dump(history, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save pomodoro history: {e}")
        return False


def log_pomodoro_completion(duration: int, task: str, interruptions: int = 0):
    """Log a completed pomodoro session."""
    entry = {
        "date": datetime.now().isoformat(),
        "duration_minutes": duration,
        "task": task,
        "interruptions": interruptions,
        "completed": True,
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.pomodoro_history.append(entry)
    save_pomodoro_history(st.session_state.pomodoro_history)


def get_todays_pomodoros() -> int:
    """Count pomodoros completed today."""
    today = datetime.now().date()
    count = 0
    for entry in st.session_state.pomodoro_history:
        entry_date = datetime.fromisoformat(entry['date']).date()
        if entry_date == today and entry.get('completed', False):
            count += 1
    return count


def get_productivity_stats(days: int = 7) -> Dict:
    """Calculate productivity statistics."""
    cutoff = datetime.now() - timedelta(days=days)
    recent = [
        e for e in st.session_state.pomodoro_history
        if datetime.fromisoformat(e['date']) >= cutoff
    ]
    
    if not recent:
        return {
            "total_pomodoros": 0,
            "total_minutes": 0,
            "avg_per_day": 0,
            "most_productive_day": "N/A"
        }
    
    total_pomodoros = len(recent)
    total_minutes = sum(e.get('duration_minutes', 0) for e in recent)
    avg_per_day = total_pomodoros / days
    
    # Find most productive day
    day_counts = {}
    for entry in recent:
        date_str = datetime.fromisoformat(entry['date']).strftime("%A")
        day_counts[date_str] = day_counts.get(date_str, 0) + 1
    
    most_productive = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else "N/A"
    
    return {
        "total_pomodoros": total_pomodoros,
        "total_minutes": total_minutes,
        "avg_per_day": avg_per_day,
        "most_productive_day": most_productive
    }


def render_timer_interface():
    """Render the main pomodoro timer interface."""
    st.markdown("### ⏱️ Pomodoro Timer")
    
    # Session configuration
    col1, col2 = st.columns(2)
    
    with col1:
        session_type = st.selectbox(
            "Session Type:",
            options=list(SESSION_TYPES.keys()),
            key="session_type_select"
        )
        
        if session_type == "Custom Duration":
            custom_duration = st.number_input(
                "Duration (minutes):",
                min_value=1,
                max_value=120,
                value=25,
                step=5,
                key="custom_duration"
            )
            work_duration = custom_duration
        else:
            work_duration = SESSION_TYPES[session_type]
        
        task_description = st.text_input(
            "What are you working on?",
            placeholder="e.g., Writing report, Studying, Coding...",
            key="task_description"
        )
    
    with col2:
        break_type = st.selectbox(
            "Break Type:",
            options=list(BREAK_TYPES.keys()),
            key="break_type_select"
        )
        
        if break_type == "Custom Break":
            custom_break = st.number_input(
                "Break Duration (minutes):",
                min_value=1,
                max_value=30,
                value=5,
                step=1,
                key="custom_break"
            )
            break_duration = custom_break
        else:
            break_duration = BREAK_TYPES[break_type]
        
        focus_sound = st.selectbox(
            "Focus Sound:",
            options=FOCUS_SOUNDS,
            key="focus_sound_select"
        )
    
    # Timer display
    st.markdown("---")
    
    if not st.session_state.pomodoro_active:
        # Start button
        if st.button("▶️ Start Pomodoro Session", use_container_width=True, type="primary"):
            if not task_description:
                st.warning("Please describe what you're working on!")
            else:
                st.session_state.pomodoro_active = True
                st.session_state.pomodoro_start_time = datetime.now()
                st.session_state.pomodoro_duration = work_duration
                st.session_state.pomodoro_type = "work"
                st.session_state.current_task = task_description
                st.session_state.break_duration = break_duration
                st.rerun()
    else:
        # Active session
        elapsed = datetime.now() - st.session_state.pomodoro_start_time
        elapsed_minutes = int(elapsed.total_seconds() / 60)
        elapsed_seconds = int(elapsed.total_seconds() % 60)
        
        remaining_minutes = st.session_state.pomodoro_duration - elapsed_minutes
        remaining_seconds = 60 - elapsed_seconds if elapsed_seconds > 0 else 0
        
        if remaining_minutes < 0:
            remaining_minutes = 0
            remaining_seconds = 0
        
        # Display timer
        if st.session_state.pomodoro_type == "work":
            st.success(f"🎯 WORK SESSION: {st.session_state.current_task}")
        else:
            st.info(f"☕ BREAK TIME: {st.session_state.break_activity}")
        
        # Large timer display
        st.markdown(f"""
        <div style='text-align: center; font-size: 72px; font-weight: bold; color: #FF6B6B; padding: 20px;'>
            {remaining_minutes:02d}:{remaining_seconds:02d}
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        progress = elapsed_minutes / st.session_state.pomodoro_duration
        st.progress(min(progress, 1.0))
        
        # Play focus sound
        if focus_sound != "None (Silent)" and st.session_state.pomodoro_type == "work":
            try:
                st.audio(f"audio_files/{focus_sound}", format="audio/wav", start_time=0)
            except:
                pass
        
        # Check if time is up
        if remaining_minutes <= 0 and remaining_seconds <= 0:
            if st.session_state.pomodoro_type == "work":
                # Work session complete - start break
                log_pomodoro_completion(
                    st.session_state.pomodoro_duration,
                    st.session_state.current_task
                )
                st.session_state.pomodoros_completed_today += 1
                st.success("🎉 Pomodoro completed! Time for a break!")
                st.balloons()
                
                st.session_state.pomodoro_type = "break"
                st.session_state.pomodoro_start_time = datetime.now()
                st.session_state.pomodoro_duration = st.session_state.break_duration
                st.rerun()
            else:
                # Break complete
                st.info("✅ Break finished! Ready for another pomodoro?")
                st.session_state.pomodoro_active = False
                st.session_state.pomodoro_start_time = None
                st.rerun()
        
        # Control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏸️ Pause", use_container_width=True):
                st.warning("Timer paused. Click Start to resume.")
        with col2:
            if st.button("⏹️ Stop Session", use_container_width=True):
                st.session_state.pomodoro_active = False
                st.session_state.pomodoro_start_time = None
                st.rerun()
        
        # Auto-refresh every second
        st_autorefresh = st.empty()
        time_module.sleep(1)
        st.rerun()


def render_mindful_break_guide():
    """Render mindful break activity guide."""
    st.markdown("### 🧘 Mindful Break Activities")
    st.info("""
    During your break, choose a restorative activity. These micro-wellness practices help you 
    truly rest and recharge, rather than just scrolling on your phone.
    """)
    
    # Activity selector
    selected_activity = st.selectbox(
        "Choose a break activity:",
        options=list(MINDFUL_BREAK_ACTIVITIES.keys()),
        key="selected_break_activity"
    )
    
    activity = MINDFUL_BREAK_ACTIVITIES[selected_activity]
    
    # Display activity details
    col1, col2 = st.columns([0.3, 0.7])
    
    with col1:
        st.markdown(f"<div style='font-size: 100px; text-align: center;'>{activity['icon']}</div>", unsafe_allow_html=True)
        st.markdown(f"**Duration:** {activity['duration']}")
        st.markdown(f"**Benefits:** {activity['benefits']}")
    
    with col2:
        st.markdown("#### Instructions:")
        for i, instruction in enumerate(activity['instructions'], 1):
            st.markdown(f"{i}. {instruction}")
    
    # Quick practice button
    if st.button(f"✨ Practice {selected_activity} Now", use_container_width=True, type="primary"):
        st.session_state.break_activity = selected_activity
        st.success(f"Great! Follow the {selected_activity} instructions above.")
        
        # Optional timer for break
        with st.expander("⏱️ Set Break Timer"):
            timer_duration = st.slider(
                "Break duration (minutes):",
                min_value=1,
                max_value=15,
                value=5,
                key="break_timer_slider"
            )
            if st.button("Start Break Timer"):
                st.info(f"Break timer set for {timer_duration} minutes. Focus on your activity!")


def render_productivity_stats():
    """Render productivity statistics and patterns."""
    st.markdown("### 📊 Productivity Statistics")
    
    # Time period selector
    period = st.selectbox(
        "View statistics for:",
        options=["Last 7 days", "Last 14 days", "Last 30 days", "All time"],
        key="stats_period"
    )
    
    days = 7 if "7" in period else (14 if "14" in period else (30 if "30" in period else 365))
    
    stats = get_productivity_stats(days)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pomodoros", stats['total_pomodoros'])
    with col2:
        hours = stats['total_minutes'] / 60
        st.metric("Total Focus Time", f"{hours:.1f}h")
    with col3:
        st.metric("Avg Per Day", f"{stats['avg_per_day']:.1f}")
    with col4:
        st.metric("Best Day", stats['most_productive_day'])
    
    # Today's progress
    st.markdown("---")
    st.markdown("### 🎯 Today's Progress")
    
    todays_count = get_todays_pomodoros()
    st.markdown(f"**Pomodoros Completed Today:** {todays_count} 🍅")
    
    # Visual representation
    pomodoro_display = "🍅 " * todays_count
    st.markdown(pomodoro_display if pomodoro_display else "No pomodoros yet today. Start your first one!")
    
    # Recent sessions
    if st.session_state.pomodoro_history:
        st.markdown("---")
        st.markdown("### 📅 Recent Sessions")
        
        recent = sorted(
            st.session_state.pomodoro_history,
            key=lambda x: x['date'],
            reverse=True
        )[:10]
        
        for session in recent:
            date_str = datetime.fromisoformat(session['date']).strftime("%b %d, %Y at %I:%M %p")
            with st.expander(f"🍅 {session.get('task', 'Unknown task')} - {date_str}"):
                st.write(f"**Duration:** {session.get('duration_minutes', 0)} minutes")
                st.write(f"**Completed:** {'✅ Yes' if session.get('completed', False) else '❌ No'}")
                if session.get('interruptions', 0) > 0:
                    st.write(f"**Interruptions:** {session['interruptions']}")


def render_tips_and_best_practices():
    """Render tips for effective pomodoro technique."""
    st.markdown("### 💡 Pomodoro Technique - Tips & Best Practices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 During Work Sessions:")
        st.success("""
        • **Single-task:** Focus on one task only
        • **Eliminate distractions:** Close unnecessary tabs, silence phone
        • **Set clear goals:** Know what you want to accomplish
        • **Use focus sounds:** Background noise can help concentration
        • **Track interruptions:** Note when you get distracted
        • **Stay committed:** Resist the urge to switch tasks
        """)
        
        st.markdown("#### 📈 Building the Habit:")
        st.info("""
        • **Start small:** Begin with 2-3 pomodoros per day
        • **Be consistent:** Same time each day helps
        • **Track progress:** Use the stats to stay motivated
        • **Adjust lengths:** Find what works for your focus span
        • **Celebrate wins:** Acknowledge completed sessions
        """)
    
    with col2:
        st.markdown("#### ☕ During Break Sessions:")
        st.warning("""
        • **Actually rest:** Don't work during breaks
        • **Move your body:** Stand, stretch, walk
        • **Mindful activities:** Use suggested break exercises
        • **Hydrate:** Drink water
        • **Avoid screens:** Give your eyes a rest
        • **Fresh air:** Open a window or step outside
        """)
        
        st.markdown("#### ⚖️ Work-Life Balance:")
        st.success("""
        • **Take longer breaks:** Every 4 pomodoros, take 15-30 min
        • **Know your limits:** Don't push beyond 8-10 pomodoros/day
        • **Listen to your body:** Fatigue means rest is needed
        • **Prevent burnout:** Structure prevents overwhelm
        • **Quality over quantity:** Focus matters more than time
        """)
    
    st.markdown("---")
    st.markdown("### 🧠 Why Pomodoro Works for Mental Health")
    
    st.info("""
    **Prevents Overwhelm:**
    - Breaking work into chunks makes big tasks manageable
    - Reduces anxiety about large projects
    - Creates sense of accomplishment with each session
    
    **Maintains Focus:**
    - Time limits increase urgency and concentration
    - Regular breaks prevent mental fatigue
    - Structured approach reduces decision fatigue
    
    **Promotes Balance:**
    - Scheduled breaks ensure rest
    - Prevents burnout from sustained work
    - Mindful breaks add wellness to productivity
    
    **Builds Awareness:**
    - Track when you're most productive
    - Identify patterns and optimize schedule
    - Learn your natural focus rhythms
    """)


def render_pomodoro_focus():
    """Main render function for Pomodoro Focus with Mindful Breaks."""
    st.header("⏱️ Pomodoro Focus with Mindful Breaks")
    
    # Initialize state
    initialize_pomodoro_state()
    
    st.info("""
    🍅 The Pomodoro Technique uses timed intervals (typically 25 minutes of focused work followed by 
    5-minute breaks) to boost productivity while preventing burnout. During breaks, we'll guide you 
    through mindful activities to ensure true rest and restoration.
    """)
    
    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "⏱️ Timer",
        "🧘 Break Activities",
        "📊 Statistics",
        "💡 Tips"
    ])
    
    with tab1:
        st.markdown("""
        Start your focused work session. The timer will guide you through work periods and breaks.
        Choose your duration, task, and optional focus sound.
        """)
        render_timer_interface()
    
    with tab2:
        st.markdown("""
        Explore mindful break activities to practice during your rest periods. These micro-wellness 
        exercises help you recharge mentally and physically.
        """)
        render_mindful_break_guide()
    
    with tab3:
        st.markdown("""
        Track your productivity patterns over time. See how many pomodoros you complete and 
        identify your most productive times.
        """)
        render_productivity_stats()
    
    with tab4:
        render_tips_and_best_practices()
    
    # Quick stats at bottom
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Today's Pomodoros", get_todays_pomodoros())
    with col2:
        week_stats = get_productivity_stats(7)
        st.metric("This Week", week_stats['total_pomodoros'])
    with col3:
        total = len(st.session_state.pomodoro_history)
        st.metric("All Time", total)
