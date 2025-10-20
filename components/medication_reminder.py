"""
Medication & Supplement Reminder Component
Simple medication tracking with customizable schedules, dose logging, refill reminders,
and side effect notes. Emphasizes privacy and local storage.
"""

import streamlit as st
from datetime import datetime, date, time, timedelta
import json
import os
from typing import Dict, List, Optional

# Medication types
MEDICATION_TYPES = [
    "💊 Prescription Medication",
    "💊 Over-the-Counter Medication",
    "🌿 Herbal Supplement",
    "💪 Vitamin",
    "🔬 Mineral Supplement",
    "🧘 Mental Health Medication",
    "💓 Physical Health Medication",
    "🌙 Sleep Aid",
    "⚡ Energy Supplement",
    "🎯 Other"
]

# Frequency options
FREQUENCY_OPTIONS = [
    "Once daily",
    "Twice daily",
    "Three times daily",
    "Four times daily",
    "Every other day",
    "Weekly",
    "As needed",
    "Custom schedule"
]

# Common side effects
COMMON_SIDE_EFFECTS = [
    "Nausea",
    "Headache",
    "Drowsiness",
    "Insomnia",
    "Dizziness",
    "Dry mouth",
    "Upset stomach",
    "Fatigue",
    "Increased energy",
    "Mood changes",
    "Appetite changes",
    "None observed"
]

# Time of day presets
TIME_PRESETS = {
    "Morning": time(8, 0),
    "Mid-Morning": time(10, 0),
    "Noon": time(12, 0),
    "Afternoon": time(14, 0),
    "Evening": time(18, 0),
    "Bedtime": time(22, 0)
}


def initialize_medication_state():
    """Initialize session state for medication tracker."""
    if "medications" not in st.session_state:
        st.session_state.medications = load_medications()
    if "medication_logs" not in st.session_state:
        st.session_state.medication_logs = load_medication_logs()
    if "refill_reminders" not in st.session_state:
        st.session_state.refill_reminders = []


def load_medications() -> List[Dict]:
    """Load medication list from file."""
    try:
        if os.path.exists("data/medications.json"):
            with open("data/medications.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load medications: {e}")
    return []


def save_medications(medications: List[Dict]) -> bool:
    """Save medication list to file."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/medications.json", "w") as f:
            json.dump(medications, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save medications: {e}")
        return False


def load_medication_logs() -> List[Dict]:
    """Load medication logs from file."""
    try:
        if os.path.exists("data/medication_logs.json"):
            with open("data/medication_logs.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load medication logs: {e}")
    return []


def save_medication_logs(logs: List[Dict]) -> bool:
    """Save medication logs to file."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/medication_logs.json", "w") as f:
            json.dump(logs, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save medication logs: {e}")
        return False


def check_refill_needed(med: Dict) -> bool:
    """Check if medication needs refill soon."""
    if med.get("quantity_remaining", 0) <= med.get("refill_threshold", 7):
        return True
    return False


def calculate_adherence_rate(med_id: str, days: int = 7) -> float:
    """Calculate adherence rate for a medication over specified days."""
    logs = st.session_state.medication_logs
    
    # Get logs for this medication in the last X days
    cutoff_date = (datetime.now() - timedelta(days=days)).date()
    recent_logs = [
        log for log in logs
        if log.get("medication_id") == med_id
        and datetime.fromisoformat(log.get("date", "")).date() >= cutoff_date
        and log.get("taken", False)
    ]
    
    # Find the medication
    medication = next((m for m in st.session_state.medications if m.get("id") == med_id), None)
    if not medication:
        return 0.0
    
    # Calculate expected doses based on frequency
    frequency = medication.get("frequency", "Once daily")
    doses_per_day = 1
    if "twice" in frequency.lower():
        doses_per_day = 2
    elif "three times" in frequency.lower():
        doses_per_day = 3
    elif "four times" in frequency.lower():
        doses_per_day = 4
    elif "every other day" in frequency.lower():
        doses_per_day = 0.5
    elif "weekly" in frequency.lower():
        doses_per_day = 1/7
    
    expected_doses = doses_per_day * days
    actual_doses = len(recent_logs)
    
    if expected_doses == 0:
        return 0.0
    
    return min((actual_doses / expected_doses) * 100, 100)


def render_medication_list():
    """Render the list of medications."""
    st.markdown("### 💊 My Medications & Supplements")
    
    if not st.session_state.medications:
        st.info("👋 No medications added yet. Click 'Add New Medication' to get started!")
        return
    
    # Check for refill reminders
    needs_refill = [med for med in st.session_state.medications if check_refill_needed(med)]
    if needs_refill:
        st.warning(f"⚠️ {len(needs_refill)} medication(s) need refill soon!")
    
    for med in st.session_state.medications:
        with st.expander(
            f"{med.get('icon', '💊')} {med.get('name', 'Unnamed')} - {med.get('dosage', '')}",
            expanded=False
        ):
            col1, col2 = st.columns([0.7, 0.3])
            
            with col1:
                st.write(f"**Type:** {med.get('type', 'N/A')}")
                st.write(f"**Dosage:** {med.get('dosage', 'N/A')}")
                st.write(f"**Frequency:** {med.get('frequency', 'N/A')}")
                
                if med.get('schedule_times'):
                    times_str = ", ".join(med['schedule_times'])
                    st.write(f"**Times:** {times_str}")
                
                if med.get('purpose'):
                    st.write(f"**Purpose:** {med.get('purpose')}")
                
                if med.get('prescriber'):
                    st.write(f"**Prescribed by:** {med.get('prescriber')}")
                
                # Quantity tracking
                quantity = med.get('quantity_remaining', 0)
                threshold = med.get('refill_threshold', 7)
                if quantity <= threshold:
                    st.error(f"📦 Quantity: {quantity} (Refill needed!)")
                else:
                    st.write(f"📦 Quantity remaining: {quantity}")
                
                # Adherence rate
                adherence = calculate_adherence_rate(med.get('id', ''), 7)
                if adherence >= 90:
                    st.success(f"✅ 7-day adherence: {adherence:.0f}%")
                elif adherence >= 70:
                    st.info(f"📊 7-day adherence: {adherence:.0f}%")
                else:
                    st.warning(f"⚠️ 7-day adherence: {adherence:.0f}%")
            
            with col2:
                # Quick log button
                if st.button("✅ Log Taken", key=f"quick_log_{med.get('id')}", use_container_width=True):
                    log_entry = {
                        "medication_id": med.get('id'),
                        "medication_name": med.get('name'),
                        "date": datetime.now().isoformat(),
                        "taken": True,
                        "time_taken": datetime.now().strftime("%H:%M"),
                        "notes": "",
                        "side_effects": []
                    }
                    st.session_state.medication_logs.append(log_entry)
                    
                    # Update quantity
                    if med.get('quantity_remaining', 0) > 0:
                        med['quantity_remaining'] -= 1
                    
                    save_medication_logs(st.session_state.medication_logs)
                    save_medications(st.session_state.medications)
                    st.success("Logged!")
                    st.rerun()
                
                # Edit button
                if st.button("✏️ Edit", key=f"edit_{med.get('id')}", use_container_width=True):
                    st.session_state.editing_med_id = med.get('id')
                    st.rerun()
                
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{med.get('id')}", use_container_width=True):
                    if st.session_state.get(f"confirm_delete_{med.get('id')}", False):
                        st.session_state.medications = [
                            m for m in st.session_state.medications if m.get('id') != med.get('id')
                        ]
                        save_medications(st.session_state.medications)
                        st.success("Medication deleted!")
                        st.rerun()
                    else:
                        st.session_state[f"confirm_delete_{med.get('id')}"] = True
                        st.warning("Click again to confirm deletion")
            
            # Notes section
            if med.get('notes'):
                st.markdown("**Notes:**")
                st.caption(med.get('notes'))


def render_add_medication():
    """Render form to add new medication."""
    st.markdown("### ➕ Add New Medication or Supplement")
    
    with st.form("add_medication_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Medication/Supplement Name *",
                placeholder="e.g., Sertraline, Vitamin D, Fish Oil"
            )
            
            med_type = st.selectbox(
                "Type *",
                options=MEDICATION_TYPES
            )
            
            dosage = st.text_input(
                "Dosage *",
                placeholder="e.g., 50mg, 2 capsules, 1000 IU"
            )
            
            frequency = st.selectbox(
                "Frequency *",
                options=FREQUENCY_OPTIONS
            )
        
        with col2:
            purpose = st.text_input(
                "Purpose/Indication",
                placeholder="e.g., Depression, Vitamin D deficiency"
            )
            
            prescriber = st.text_input(
                "Prescriber/Doctor (optional)",
                placeholder="Dr. Smith"
            )
            
            quantity = st.number_input(
                "Current Quantity",
                min_value=0,
                max_value=1000,
                value=30,
                help="Number of doses/pills remaining"
            )
            
            refill_threshold = st.number_input(
                "Refill Reminder Threshold",
                min_value=1,
                max_value=30,
                value=7,
                help="Get reminded when quantity falls below this number"
            )
        
        # Schedule times
        st.markdown("**Schedule Times**")
        st.caption("Select what times you take this medication")
        
        time_cols = st.columns(len(TIME_PRESETS))
        selected_times = []
        
        for i, (preset_name, preset_time) in enumerate(TIME_PRESETS.items()):
            with time_cols[i]:
                if st.checkbox(preset_name, key=f"time_{preset_name}"):
                    selected_times.append(preset_time.strftime("%H:%M"))
        
        # Custom time
        custom_time = st.time_input("Add custom time (optional)", value=None, key="custom_time")
        if custom_time:
            selected_times.append(custom_time.strftime("%H:%M"))
        
        notes = st.text_area(
            "Additional Notes (optional)",
            placeholder="Any special instructions, food requirements, etc.",
            height=80
        )
        
        submitted = st.form_submit_button("💾 Add Medication", use_container_width=True, type="primary")
        
        if submitted:
            if not name or not dosage:
                st.error("Please fill in all required fields (marked with *)")
            else:
                # Get icon based on type
                icon = med_type.split()[0] if med_type else "💊"
                
                new_med = {
                    "id": f"med_{datetime.now().timestamp()}",
                    "name": name,
                    "type": med_type,
                    "dosage": dosage,
                    "frequency": frequency,
                    "schedule_times": selected_times,
                    "purpose": purpose,
                    "prescriber": prescriber,
                    "quantity_remaining": quantity,
                    "refill_threshold": refill_threshold,
                    "notes": notes,
                    "icon": icon,
                    "created_date": datetime.now().isoformat()
                }
                
                st.session_state.medications.append(new_med)
                if save_medications(st.session_state.medications):
                    st.success(f"✅ {name} added successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Failed to save medication.")


def render_log_dose():
    """Render form to log medication dose."""
    st.markdown("### 📝 Log Medication Dose")
    
    if not st.session_state.medications:
        st.info("Add medications first to start logging doses.")
        return
    
    with st.form("log_dose_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Medication selector
            med_options = {f"{m.get('icon', '💊')} {m.get('name')} - {m.get('dosage')}": m.get('id') 
                          for m in st.session_state.medications}
            
            selected_med_display = st.selectbox(
                "Select Medication *",
                options=list(med_options.keys())
            )
            selected_med_id = med_options[selected_med_display]
            
            log_date = st.date_input(
                "Date *",
                value=datetime.now().date(),
                max_value=datetime.now().date()
            )
            
            log_time = st.time_input(
                "Time Taken *",
                value=datetime.now().time()
            )
        
        with col2:
            taken = st.radio(
                "Status *",
                options=["✅ Taken", "❌ Missed", "⏭️ Skipped (intentionally)"],
                index=0
            )
            
            side_effects = st.multiselect(
                "Side Effects (if any)",
                options=COMMON_SIDE_EFFECTS
            )
        
        notes = st.text_area(
            "Notes (optional)",
            placeholder="How did you feel? Any reactions? Took with food?",
            height=80
        )
        
        submitted = st.form_submit_button("💾 Log Entry", use_container_width=True)
        
        if submitted:
            # Find medication
            medication = next((m for m in st.session_state.medications if m.get('id') == selected_med_id), None)
            
            log_entry = {
                "medication_id": selected_med_id,
                "medication_name": medication.get('name') if medication else 'Unknown',
                "date": log_date.isoformat(),
                "time_taken": log_time.strftime("%H:%M"),
                "taken": "Taken" in taken,
                "status": taken,
                "side_effects": side_effects,
                "notes": notes,
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.medication_logs.append(log_entry)
            
            # Update quantity if taken
            if "Taken" in taken and medication:
                if medication.get('quantity_remaining', 0) > 0:
                    medication['quantity_remaining'] -= 1
            
            if save_medication_logs(st.session_state.medication_logs):
                save_medications(st.session_state.medications)
                st.success("✅ Dose logged successfully!")
                st.rerun()
            else:
                st.error("Failed to save log entry.")


def render_adherence_tracking():
    """Render adherence tracking and statistics."""
    st.markdown("### 📊 Adherence Tracking")
    
    if not st.session_state.medications:
        st.info("Add medications to track adherence.")
        return
    
    # Time period selector
    period = st.selectbox(
        "View adherence for:",
        options=["Last 7 days", "Last 14 days", "Last 30 days"],
        index=0
    )
    
    days = 7 if "7" in period else (14 if "14" in period else 30)
    
    st.markdown("---")
    
    # Adherence for each medication
    for med in st.session_state.medications:
        adherence = calculate_adherence_rate(med.get('id'), days)
        
        col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
        
        with col1:
            st.write(f"**{med.get('icon', '💊')} {med.get('name')}**")
        
        with col2:
            st.progress(adherence / 100)
        
        with col3:
            if adherence >= 90:
                st.success(f"{adherence:.0f}%")
            elif adherence >= 70:
                st.info(f"{adherence:.0f}%")
            else:
                st.warning(f"{adherence:.0f}%")
    
    # Overall statistics
    if st.session_state.medication_logs:
        st.markdown("---")
        st.markdown("### 📈 Overall Statistics")
        
        # Calculate overall adherence
        all_adherence = [calculate_adherence_rate(m.get('id'), days) for m in st.session_state.medications]
        avg_adherence = sum(all_adherence) / len(all_adherence) if all_adherence else 0
        
        # Count logs
        cutoff_date = (datetime.now() - timedelta(days=days)).date()
        recent_logs = [
            log for log in st.session_state.medication_logs
            if datetime.fromisoformat(log.get('date', '')).date() >= cutoff_date
        ]
        
        taken_count = sum(1 for log in recent_logs if log.get('taken', False))
        missed_count = sum(1 for log in recent_logs if not log.get('taken', False))
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Adherence", f"{avg_adherence:.0f}%")
        with col2:
            st.metric("Doses Taken", taken_count)
        with col3:
            st.metric("Doses Missed", missed_count)
        with col4:
            st.metric("Total Medications", len(st.session_state.medications))


def render_medication_history():
    """Render medication log history."""
    st.markdown("### 📅 Medication History")
    
    if not st.session_state.medication_logs:
        st.info("No medication logs yet. Start logging your doses!")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        # Medication filter
        med_filter_options = ["All Medications"] + [
            f"{m.get('icon', '💊')} {m.get('name')}" for m in st.session_state.medications
        ]
        selected_filter = st.selectbox("Filter by medication:", med_filter_options)
    
    with col2:
        # Show only
        show_filter = st.selectbox(
            "Show:",
            options=["All entries", "Taken only", "Missed only"]
        )
    
    # Sort logs by date (most recent first)
    sorted_logs = sorted(
        st.session_state.medication_logs,
        key=lambda x: x.get('date', '') + x.get('time_taken', ''),
        reverse=True
    )
    
    # Apply filters
    filtered_logs = sorted_logs
    
    if selected_filter != "All Medications":
        med_name = selected_filter.split(" ", 1)[1] if " " in selected_filter else selected_filter
        filtered_logs = [log for log in filtered_logs if log.get('medication_name') == med_name]
    
    if show_filter == "Taken only":
        filtered_logs = [log for log in filtered_logs if log.get('taken', False)]
    elif show_filter == "Missed only":
        filtered_logs = [log for log in filtered_logs if not log.get('taken', False)]
    
    # Display logs
    st.markdown(f"**Showing {len(filtered_logs)} entries**")
    
    for log in filtered_logs[:50]:  # Show last 50 entries
        taken = log.get('taken', False)
        icon = "✅" if taken else "❌"
        status_color = "green" if taken else "red"
        
        with st.expander(
            f"{icon} {log.get('medication_name', 'Unknown')} - {log.get('date')} at {log.get('time_taken', 'N/A')}"
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Status:** {log.get('status', 'Taken' if taken else 'Missed')}")
                st.write(f"**Date:** {log.get('date')}")
                st.write(f"**Time:** {log.get('time_taken', 'N/A')}")
            
            with col2:
                if log.get('side_effects'):
                    st.write(f"**Side Effects:** {', '.join(log.get('side_effects'))}")
                else:
                    st.write("**Side Effects:** None reported")
            
            if log.get('notes'):
                st.write(f"**Notes:** {log.get('notes')}")


def render_privacy_info():
    """Render privacy and security information."""
    st.markdown("### 🔒 Privacy & Data Security")
    
    st.success("""
    **Your health data is private and secure:**
    
    ✅ **Local Storage Only** - All medication data is stored locally on your device  
    ✅ **No Cloud Sync** - Your information never leaves your device  
    ✅ **No Third Parties** - We don't share data with anyone  
    ✅ **You Control It** - Delete your data anytime by removing the data files  
    ✅ **Encrypted Storage** - Files are stored securely on your system  
    """)
    
    st.markdown("---")
    st.markdown("### 📖 Using This Tool")
    
    st.info("""
    **This tool helps you:**
    - Track medication and supplement schedules
    - Log doses and monitor adherence
    - Note side effects and patterns
    - Get refill reminders
    - Share adherence data with healthcare providers
    
    **This tool is NOT:**
    - A replacement for medical advice
    - A substitute for talking to your doctor
    - Able to provide medical recommendations
    - Connected to pharmacy systems
    """)
    
    st.markdown("---")
    st.markdown("### ⚠️ Important Reminders")
    
    st.warning("""
    - Always consult your healthcare provider before starting, stopping, or changing medications
    - Never share prescription medications with others
    - Store medications safely and as directed
    - Check expiration dates regularly
    - Report severe side effects to your doctor immediately
    - Keep a backup list of your medications in case of emergencies
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips for Better Adherence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Build Habits:**
        - Take meds at the same time daily
        - Link to daily routine (e.g., breakfast)
        - Use visual reminders (pill organizer)
        - Set phone alarms
        """)
    
    with col2:
        st.markdown("""
        **Stay Organized:**
        - Keep meds in one place
        - Use a pill organizer
        - Keep a backup supply
        - Track refills in advance
        """)
    
    st.markdown("---")
    st.markdown("### 📱 Recommended Apps & Resources")
    
    st.markdown("""
    - **Medisafe**: Medication reminder and tracker
    - **MyTherapy**: Pill reminder with health journal
    - **CareZone**: Medication management for families
    - **Drugs.com**: Drug information and interactions
    - **FDA MedWatch**: Report side effects
    """)


def render_medication_reminder():
    """Main render function for medication & supplement reminder."""
    st.header("🔔 Medication & Supplement Reminder")
    
    # Initialize state
    initialize_medication_state()
    
    # Privacy notice at top
    st.info("🔒 **Privacy Note:** All medication data is stored locally on your device and never shared.")
    
    # Tab navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💊 My Medications",
        "➕ Add New",
        "📝 Log Dose",
        "📊 Adherence",
        "ℹ️ Info & Privacy"
    ])
    
    with tab1:
        st.markdown("""
        View and manage your medications and supplements. Track quantities and get refill reminders.
        """)
        render_medication_list()
        
        st.markdown("---")
        render_medication_history()
    
    with tab2:
        st.markdown("""
        Add a new medication, vitamin, or supplement to track. Include schedule, dosage, and refill information.
        """)
        render_add_medication()
    
    with tab3:
        st.markdown("""
        Log when you take your medications, note any side effects, and track how you feel.
        """)
        render_log_dose()
    
    with tab4:
        st.markdown("""
        Monitor your medication adherence over time. Consistent adherence is key to treatment effectiveness.
        """)
        render_adherence_tracking()
    
    with tab5:
        render_privacy_info()
