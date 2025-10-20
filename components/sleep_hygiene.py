"""
Sleep Hygiene Toolkit Component
Comprehensive sleep improvement tool with bedtime routine builder, sleep quality tracker,
and educational content about sleep's impact on mental health.
"""

import streamlit as st
from datetime import datetime, time, timedelta
import json
import os
from typing import Dict, List, Optional

# Sleep hygiene best practices
SLEEP_HYGIENE_TIPS = {
    "Environment": {
        "icon": "🛏️",
        "tips": [
            "Keep bedroom temperature between 60-67°F (15-19°C)",
            "Use blackout curtains or eye mask for complete darkness",
            "Reduce noise or use white noise machine",
            "Invest in comfortable mattress and pillows",
            "Keep bedroom clean and clutter-free",
            "Use bedroom only for sleep and intimacy (not work/TV)"
        ]
    },
    "Routine": {
        "icon": "📅",
        "tips": [
            "Go to bed and wake up at the same time every day",
            "Allow 7-9 hours for sleep each night",
            "Create a relaxing pre-sleep routine (30-60 minutes)",
            "Avoid napping after 3 PM or limit to 20-30 minutes",
            "Get morning sunlight exposure within 30 minutes of waking",
            "Exercise regularly but not within 3 hours of bedtime"
        ]
    },
    "Diet": {
        "icon": "☕",
        "tips": [
            "Avoid caffeine 6-8 hours before bedtime",
            "Limit alcohol, especially close to bedtime",
            "Avoid large meals 2-3 hours before sleep",
            "Consider light snack if hungry (complex carbs + protein)",
            "Stay hydrated but reduce fluids 2 hours before bed",
            "Avoid nicotine, especially in the evening"
        ]
    },
    "Technology": {
        "icon": "📱",
        "tips": [
            "Avoid screens 1-2 hours before bedtime",
            "Use blue light filters on devices in evening",
            "Keep phone out of bedroom or in silent mode",
            "Charge devices outside the bedroom",
            "Use traditional alarm clock instead of phone",
            "Avoid stimulating content (news, work emails) before bed"
        ]
    },
    "Mental": {
        "icon": "🧠",
        "tips": [
            "Practice relaxation techniques (breathing, meditation)",
            "Write down worries/tasks before bed (worry journal)",
            "Use visualization or guided imagery",
            "Try progressive muscle relaxation",
            "If can't sleep after 20 minutes, get up and do relaxing activity",
            "Avoid clock-watching - remove visible clocks from bedroom"
        ]
    }
}

# Wind-down activities
WIND_DOWN_ACTIVITIES = [
    {"name": "Reading (physical book)", "duration": "20-30 min", "icon": "📚"},
    {"name": "Gentle stretching or yoga", "duration": "10-15 min", "icon": "🧘"},
    {"name": "Meditation or breathing exercises", "duration": "10-20 min", "icon": "🧘‍♀️"},
    {"name": "Warm bath or shower", "duration": "15-20 min", "icon": "🛁"},
    {"name": "Listening to calming music", "duration": "15-30 min", "icon": "🎵"},
    {"name": "Journaling or gratitude practice", "duration": "10-15 min", "icon": "✍️"},
    {"name": "Light housekeeping or organizing", "duration": "10-15 min", "icon": "🧹"},
    {"name": "Herbal tea and relaxation", "duration": "15-20 min", "icon": "🍵"},
    {"name": "Gentle conversation with loved ones", "duration": "15-30 min", "icon": "💬"},
    {"name": "Aromatherapy (lavender, chamomile)", "duration": "Ongoing", "icon": "🌸"}
]

# Sleep quality factors
SLEEP_QUALITY_FACTORS = [
    "Difficulty falling asleep (>30 min)",
    "Woke up during night",
    "Woke up too early",
    "Felt refreshed upon waking",
    "Dreamt or remembered dreams",
    "Had nightmares",
    "Snoring or breathing issues",
    "Physical discomfort or pain",
    "Noise disturbances",
    "Temperature issues (too hot/cold)"
]


def initialize_sleep_state():
    """Initialize session state for sleep toolkit."""
    if "sleep_tracker_data" not in st.session_state:
        st.session_state.sleep_tracker_data = load_sleep_data()
    if "bedtime_routine" not in st.session_state:
        st.session_state.bedtime_routine = load_bedtime_routine()
    if "sleep_goals" not in st.session_state:
        st.session_state.sleep_goals = {
            "target_bedtime": time(22, 30),
            "target_wake_time": time(6, 30),
            "target_hours": 8.0
        }


def load_sleep_data() -> List[Dict]:
    """Load sleep tracking data from file."""
    try:
        if os.path.exists("data/sleep_tracker.json"):
            with open("data/sleep_tracker.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load sleep data: {e}")
    return []


def save_sleep_data(data: List[Dict]) -> bool:
    """Save sleep tracking data to file."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/sleep_tracker.json", "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save sleep data: {e}")
        return False


def load_bedtime_routine() -> List[Dict]:
    """Load bedtime routine from file."""
    try:
        if os.path.exists("data/bedtime_routine.json"):
            with open("data/bedtime_routine.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load routine: {e}")
    return []


def save_bedtime_routine(routine: List[Dict]) -> bool:
    """Save bedtime routine to file."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/bedtime_routine.json", "w") as f:
            json.dump(routine, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save routine: {e}")
        return False


def calculate_sleep_duration(bedtime: time, wake_time: time) -> float:
    """Calculate sleep duration in hours."""
    bed_minutes = bedtime.hour * 60 + bedtime.minute
    wake_minutes = wake_time.hour * 60 + wake_time.minute
    
    if wake_minutes <= bed_minutes:
        # Crossed midnight
        wake_minutes += 24 * 60
    
    duration_minutes = wake_minutes - bed_minutes
    return duration_minutes / 60


def calculate_caffeine_cutoff(bedtime: time, hours_before: int = 6) -> time:
    """Calculate when to stop caffeine intake."""
    bed_datetime = datetime.combine(datetime.today(), bedtime)
    cutoff_datetime = bed_datetime - timedelta(hours=hours_before)
    return cutoff_datetime.time()


def render_sleep_education():
    """Render educational content about sleep and mental health."""
    st.markdown("### 📚 Why Sleep Matters for Mental Health")
    
    st.info("""
    **Sleep and mental health are deeply interconnected:**
    - Poor sleep increases risk of depression and anxiety
    - Mental health conditions often cause sleep problems
    - Quality sleep improves mood regulation and emotional resilience
    - Sleep deprivation impairs cognitive function and decision-making
    - Good sleep hygiene is a foundational pillar of mental wellness
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**😴 Sleep Deprivation Effects**")
        st.markdown("""
        - Increased irritability
        - Poor concentration
        - Memory problems
        - Weakened immune system
        - Higher stress levels
        - Impaired judgment
        """)
    
    with col2:
        st.markdown("**✨ Quality Sleep Benefits**")
        st.markdown("""
        - Better mood regulation
        - Enhanced memory
        - Improved focus
        - Stronger immunity
        - Reduced anxiety
        - Better physical health
        """)
    
    with col3:
        st.markdown("**🎯 Sleep Recommendations**")
        st.markdown("""
        - Adults: 7-9 hours
        - Consistent schedule
        - Dark, cool, quiet room
        - Regular exercise
        - Stress management
        - Healthy diet
        """)


def render_sleep_tracker():
    """Render sleep quality tracker."""
    st.markdown("### 📊 Sleep Quality Tracker")
    st.caption("Log your sleep to identify patterns and track improvements.")
    
    with st.form("sleep_log_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            log_date = st.date_input(
                "Date:",
                value=datetime.now().date() - timedelta(days=1),
                max_value=datetime.now().date()
            )
            
            bedtime = st.time_input(
                "🌙 Bedtime:",
                value=time(22, 30),
                help="What time did you go to bed?"
            )
            
            wake_time = st.time_input(
                "☀️ Wake time:",
                value=time(6, 30),
                help="What time did you wake up?"
            )
        
        with col2:
            sleep_quality = st.slider(
                "Overall sleep quality:",
                min_value=1,
                max_value=10,
                value=5,
                help="1 = Very poor, 10 = Excellent"
            )
            
            time_to_fall_asleep = st.number_input(
                "Minutes to fall asleep:",
                min_value=0,
                max_value=180,
                value=15,
                step=5
            )
            
            times_woken = st.number_input(
                "Times woken during night:",
                min_value=0,
                max_value=20,
                value=0,
                step=1
            )
        
        st.markdown("**Sleep factors (select all that apply):**")
        factors = st.multiselect(
            "Factors:",
            options=SLEEP_QUALITY_FACTORS,
            default=[]
        )
        
        notes = st.text_area(
            "Additional notes (optional):",
            placeholder="e.g., had coffee late, stressful day, new pillow...",
            height=80
        )
        
        submitted = st.form_submit_button("💾 Log Sleep Entry", use_container_width=True)
        
        if submitted:
            sleep_duration = calculate_sleep_duration(bedtime, wake_time)
            
            entry = {
                "date": log_date.isoformat(),
                "bedtime": bedtime.strftime("%H:%M"),
                "wake_time": wake_time.strftime("%H:%M"),
                "duration_hours": round(sleep_duration, 2),
                "quality": sleep_quality,
                "time_to_sleep": time_to_fall_asleep,
                "times_woken": times_woken,
                "factors": factors,
                "notes": notes,
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.sleep_tracker_data.append(entry)
            if save_sleep_data(st.session_state.sleep_tracker_data):
                st.success(f"✅ Sleep entry for {log_date} logged successfully!")
                st.balloons()
            else:
                st.error("Failed to save sleep entry.")
    
    # Display recent entries
    if st.session_state.sleep_tracker_data:
        st.markdown("---")
        st.markdown("### 📅 Recent Sleep Logs")
        
        # Show last 7 entries
        recent_entries = sorted(
            st.session_state.sleep_tracker_data,
            key=lambda x: x.get('date', ''),
            reverse=True
        )[:7]
        
        for entry in recent_entries:
            with st.expander(
                f"📆 {entry['date']} - Quality: {entry['quality']}/10 - Duration: {entry['duration_hours']}h"
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"🌙 Bedtime: {entry['bedtime']}")
                    st.write(f"☀️ Wake time: {entry['wake_time']}")
                    st.write(f"⏱️ Time to fall asleep: {entry['time_to_sleep']} min")
                with col2:
                    st.write(f"💤 Duration: {entry['duration_hours']} hours")
                    st.write(f"🌃 Times woken: {entry['times_woken']}")
                    st.write(f"⭐ Quality: {entry['quality']}/10")
                
                if entry.get('factors'):
                    st.write(f"**Factors:** {', '.join(entry['factors'])}")
                if entry.get('notes'):
                    st.write(f"**Notes:** {entry['notes']}")
        
        # Statistics
        if len(st.session_state.sleep_tracker_data) >= 3:
            st.markdown("---")
            st.markdown("### 📈 Sleep Statistics")
            
            durations = [e['duration_hours'] for e in st.session_state.sleep_tracker_data]
            qualities = [e['quality'] for e in st.session_state.sleep_tracker_data]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Average Duration", f"{sum(durations)/len(durations):.1f}h")
            with col2:
                st.metric("Average Quality", f"{sum(qualities)/len(qualities):.1f}/10")
            with col3:
                st.metric("Total Entries", len(st.session_state.sleep_tracker_data))
            with col4:
                recent_avg = sum(qualities[-7:])/min(7, len(qualities))
                st.metric("Recent Quality (7d)", f"{recent_avg:.1f}/10")


def render_bedtime_routine_builder():
    """Render bedtime routine builder."""
    st.markdown("### 🌙 Bedtime Routine Builder")
    st.caption("Create your personalized wind-down routine for better sleep.")
    
    # Display current routine
    if st.session_state.bedtime_routine:
        st.markdown("#### Your Current Routine")
        total_duration = 0
        for i, activity in enumerate(st.session_state.bedtime_routine):
            col1, col2, col3 = st.columns([0.6, 0.3, 0.1])
            with col1:
                st.write(f"{i+1}. {activity['icon']} {activity['name']}")
            with col2:
                st.write(f"⏱️ {activity['duration']}")
            with col3:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.bedtime_routine.pop(i)
                    save_bedtime_routine(st.session_state.bedtime_routine)
                    st.rerun()
        
        st.markdown("---")
    
    # Add new activity
    st.markdown("#### Add Activity to Routine")
    
    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
        activity_options = [f"{a['icon']} {a['name']}" for a in WIND_DOWN_ACTIVITIES]
        selected_activity = st.selectbox(
            "Choose an activity:",
            options=activity_options,
            key="activity_selector"
        )
    
    with col2:
        custom_duration = st.text_input(
            "Duration:",
            value="15 min",
            key="duration_input"
        )
    
    if st.button("➕ Add to Routine", use_container_width=True):
        # Find the selected activity
        for activity in WIND_DOWN_ACTIVITIES:
            if f"{activity['icon']} {activity['name']}" == selected_activity:
                new_activity = {
                    "name": activity['name'],
                    "icon": activity['icon'],
                    "duration": custom_duration
                }
                st.session_state.bedtime_routine.append(new_activity)
                if save_bedtime_routine(st.session_state.bedtime_routine):
                    st.success(f"✅ Added {activity['name']} to your routine!")
                    st.rerun()
                break
    
    # Suggested routines
    with st.expander("💡 See Suggested Routines"):
        st.markdown("**Relaxation-Focused Routine (60 min)**")
        st.write("1. 🛁 Warm bath (20 min)")
        st.write("2. 🍵 Herbal tea (10 min)")
        st.write("3. 📚 Reading (20 min)")
        st.write("4. 🧘‍♀️ Meditation (10 min)")
        
        st.markdown("**Quick Wind-Down (30 min)**")
        st.write("1. 🧹 Light tidying (10 min)")
        st.write("2. 🧘 Gentle stretching (10 min)")
        st.write("3. ✍️ Journaling (10 min)")
        
        st.markdown("**Sleep-Prep Routine (45 min)**")
        st.write("1. 🎵 Calming music (15 min)")
        st.write("2. 🌸 Aromatherapy prep (5 min)")
        st.write("3. 📚 Reading (15 min)")
        st.write("4. 🧘‍♀️ Breathing exercises (10 min)")


def render_sleep_environment_checklist():
    """Render sleep environment checklist."""
    st.markdown("### ✅ Sleep Environment Checklist")
    st.caption("Optimize your bedroom for better sleep quality.")
    
    checklist_state_key = "sleep_environment_checklist"
    if checklist_state_key not in st.session_state:
        st.session_state[checklist_state_key] = {}
    
    for category, data in SLEEP_HYGIENE_TIPS.items():
        with st.expander(f"{data['icon']} {category}", expanded=False):
            for i, tip in enumerate(data['tips']):
                key = f"{category}_{i}"
                checked = st.session_state[checklist_state_key].get(key, False)
                if st.checkbox(tip, value=checked, key=f"check_{key}"):
                    st.session_state[checklist_state_key][key] = True
                else:
                    st.session_state[checklist_state_key][key] = False
    
    # Show progress
    total_tips = sum(len(data['tips']) for data in SLEEP_HYGIENE_TIPS.values())
    checked_tips = sum(1 for v in st.session_state[checklist_state_key].values() if v)
    progress = checked_tips / total_tips if total_tips > 0 else 0
    
    st.markdown("---")
    st.markdown("### 📊 Your Sleep Hygiene Score")
    st.progress(progress)
    st.write(f"**{checked_tips}/{total_tips}** practices implemented ({progress*100:.0f}%)")
    
    if progress == 1.0:
        st.success("🎉 Excellent! You're following all sleep hygiene best practices!")
    elif progress >= 0.7:
        st.info("👍 Great job! You're following most sleep hygiene practices.")
    elif progress >= 0.4:
        st.warning("💪 Good start! Keep working on improving your sleep environment.")
    else:
        st.error("🎯 There's room for improvement. Start with a few key changes!")


def render_sleep_schedule_planner():
    """Render sleep schedule planner."""
    st.markdown("### ⏰ Sleep Schedule Planner")
    st.caption("Plan your ideal sleep schedule based on your lifestyle.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_wake_time = st.time_input(
            "🌅 Desired wake time:",
            value=st.session_state.sleep_goals['target_wake_time'],
            help="What time do you need to wake up?"
        )
        
        target_hours = st.slider(
            "🎯 Target sleep duration (hours):",
            min_value=6.0,
            max_value=10.0,
            value=st.session_state.sleep_goals['target_hours'],
            step=0.5,
            help="Recommended: 7-9 hours for adults"
        )
    
    with col2:
        # Calculate recommended bedtime
        wake_datetime = datetime.combine(datetime.today(), target_wake_time)
        sleep_duration = timedelta(hours=target_hours)
        bedtime_datetime = wake_datetime - sleep_duration
        recommended_bedtime = bedtime_datetime.time()
        
        st.markdown("#### 💤 Recommended Schedule")
        st.info(f"""
        **Bedtime:** {recommended_bedtime.strftime('%I:%M %p')}  
        **Wake time:** {target_wake_time.strftime('%I:%M %p')}  
        **Sleep duration:** {target_hours} hours
        """)
        
        # Calculate wind-down and caffeine cutoff
        wind_down_time = (bedtime_datetime - timedelta(minutes=30)).time()
        caffeine_cutoff = calculate_caffeine_cutoff(recommended_bedtime, 6)
        
        st.markdown("#### 🎯 Important Times")
        st.write(f"🚫 Caffeine cutoff: **{caffeine_cutoff.strftime('%I:%M %p')}**")
        st.write(f"🌙 Start wind-down: **{wind_down_time.strftime('%I:%M %p')}**")
        st.write(f"📱 Screens off: **{wind_down_time.strftime('%I:%M %p')}**")
    
    if st.button("💾 Save Sleep Goals", use_container_width=True):
        st.session_state.sleep_goals = {
            "target_bedtime": recommended_bedtime,
            "target_wake_time": target_wake_time,
            "target_hours": target_hours
        }
        st.success("✅ Sleep goals saved!")
    
    # Tips for maintaining schedule
    st.markdown("---")
    st.markdown("### 💡 Tips for Consistent Schedule")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Building the Habit:**
        - Start gradually (15-30 min adjustments)
        - Be consistent, even on weekends
        - Use alarms for bedtime reminders
        - Prepare the night before
        """)
    
    with col2:
        st.markdown("""
        **If You Can't Sleep:**
        - Don't force it - get up after 20 min
        - Do a calm activity in dim light
        - Return to bed when sleepy
        - Avoid checking the time
        """)


def render_sleep_hygiene_toolkit():
    """Main render function for sleep hygiene toolkit."""
    st.header("🌙 Sleep Hygiene Toolkit")
    
    # Initialize state
    initialize_sleep_state()
    
    # Tab navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Track Sleep",
        "🌙 Bedtime Routine",
        "⏰ Sleep Schedule",
        "✅ Environment Check",
        "📚 Education",
        "💡 Quick Tips"
    ])
    
    with tab1:
        st.markdown("""
        Track your sleep patterns to identify what helps or hinders your rest. 
        Consistent logging helps you discover personal sleep insights.
        """)
        render_sleep_tracker()
    
    with tab2:
        st.markdown("""
        Build a personalized bedtime routine to signal your body it's time to wind down. 
        A consistent routine improves sleep quality and reduces time to fall asleep.
        """)
        render_bedtime_routine_builder()
    
    with tab3:
        st.markdown("""
        Plan your ideal sleep schedule based on your lifestyle and sleep needs. 
        Consistency is key - try to maintain the same schedule every day.
        """)
        render_sleep_schedule_planner()
    
    with tab4:
        st.markdown("""
        Optimize your bedroom environment for better sleep. Small changes can make 
        a big difference in sleep quality.
        """)
        render_sleep_environment_checklist()
    
    with tab5:
        render_sleep_education()
    
    with tab6:
        st.markdown("### 💡 Quick Sleep Hygiene Tips")
        
        st.markdown("#### 🌅 Morning Routine")
        st.info("""
        - Wake up at the same time daily (even weekends)
        - Get sunlight exposure within 30 minutes
        - Eat a healthy breakfast
        - Exercise if possible (but not too close to bedtime)
        """)
        
        st.markdown("#### 🌆 Evening Routine")
        st.info("""
        - Dim lights 2-3 hours before bed
        - Avoid large meals 2-3 hours before sleep
        - Stop caffeine 6-8 hours before bedtime
        - Begin wind-down routine 30-60 minutes before bed
        - Keep bedroom cool (60-67°F / 15-19°C)
        """)
        
        st.markdown("#### 🚫 Things to Avoid")
        st.warning("""
        - Screens (blue light) before bed
        - Stimulating activities close to bedtime
        - Clock-watching if you can't sleep
        - Alcohol as a sleep aid (disrupts sleep quality)
        - Napping late in the day
        - Using bedroom for work or watching TV
        """)
        
        st.markdown("#### 🆘 When to Seek Help")
        st.error("""
        Consider consulting a healthcare provider if you experience:
        - Persistent insomnia (>3 nights/week for >3 months)
        - Excessive daytime sleepiness despite adequate sleep
        - Loud snoring or breathing pauses during sleep
        - Unusual movements or behaviors during sleep
        - Extreme difficulty waking up or staying awake
        - Sleep problems significantly affecting daily life
        """)
        
        st.markdown("---")
        st.markdown("#### 📱 Sleep Apps & Resources")
        st.markdown("""
        - **Sleep Cycle**: Sleep tracking and smart alarm
        - **Calm**: Meditation and sleep stories
        - **Headspace**: Guided meditation for sleep
        - **Rain Rain**: Ambient sounds for sleep
        - **National Sleep Foundation**: sleepfoundation.org
        """)
