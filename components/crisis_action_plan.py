"""
Acute Crisis Action Plan Builder Component
Help users create a personalized safety plan for mental health crises.
Includes warning signs, coping strategies, contacts, professional resources,
reasons for living, and environment safety steps.
"""

import streamlit as st
from datetime import datetime, date
import json
import os
from typing import Dict, List, Optional

# Pre-defined warning signs
COMMON_WARNING_SIGNS = [
    "Feeling hopeless or worthless",
    "Overwhelming sadness or anxiety",
    "Thoughts of self-harm or suicide",
    "Inability to sleep or sleeping too much",
    "Loss of interest in activities I usually enjoy",
    "Withdrawal from friends and family",
    "Extreme mood swings",
    "Difficulty concentrating or making decisions",
    "Increased use of alcohol or drugs",
    "Feeling like a burden to others",
    "Making preparations or saying goodbye",
    "Reckless or impulsive behavior"
]

# Internal coping strategies
INTERNAL_COPING_STRATEGIES = [
    "Deep breathing exercises",
    "Progressive muscle relaxation",
    "Mindfulness meditation",
    "Counting backwards from 100",
    "Grounding techniques (5-4-3-2-1)",
    "Listening to calming music",
    "Taking a warm bath or shower",
    "Writing in a journal",
    "Reciting positive affirmations",
    "Visualizing a safe place",
    "Using aromatherapy (lavender, chamomile)",
    "Gentle stretching or yoga"
]

# Distraction activities
DISTRACTION_ACTIVITIES = [
    "Call or text a friend",
    "Go for a walk",
    "Watch a comforting movie or TV show",
    "Read a book",
    "Do a puzzle or brain game",
    "Listen to a podcast",
    "Cook or bake something",
    "Do a creative activity (draw, paint, craft)",
    "Play with a pet",
    "Clean or organize a space",
    "Exercise (even gentle movement)",
    "Take photos or look at photo albums"
]

# Environment safety steps
SAFETY_STEPS = [
    "Remove or secure means of self-harm (medications, sharp objects, weapons)",
    "Tell someone I trust that I'm struggling",
    "Stay in a safe, public place if needed",
    "Avoid alcohol and drugs",
    "Create a comfortable, calming environment",
    "Keep emergency numbers easily accessible",
    "Have a crisis kit prepared (comfort items, contacts, coping tools)",
    "Identify safe spaces to go to",
    "Remove triggers from immediate environment",
    "Ask someone to stay with me"
]

# Professional resources
PROFESSIONAL_RESOURCES = [
    {
        "name": "National Suicide Prevention Lifeline (US)",
        "number": "988",
        "available": "24/7",
        "description": "Free and confidential support"
    },
    {
        "name": "Crisis Text Line (US)",
        "number": "Text HOME to 741741",
        "available": "24/7",
        "description": "Text-based crisis support"
    },
    {
        "name": "Emergency Services",
        "number": "911 (US) / 999 (UK) / 112 (EU)",
        "available": "24/7",
        "description": "For immediate life-threatening emergencies"
    },
    {
        "name": "SAMHSA National Helpline",
        "number": "1-800-662-4357",
        "available": "24/7",
        "description": "Mental health and substance abuse"
    },
    {
        "name": "Veterans Crisis Line",
        "number": "988 then Press 1",
        "available": "24/7",
        "description": "Support for veterans"
    },
    {
        "name": "Trevor Project (LGBTQ Youth)",
        "number": "1-866-488-7386",
        "available": "24/7",
        "description": "LGBTQ youth crisis support"
    }
]


def initialize_crisis_plan_state():
    """Initialize session state for crisis plan."""
    if "crisis_plan" not in st.session_state:
        st.session_state.crisis_plan = load_crisis_plan()
    if "plan_last_reviewed" not in st.session_state:
        st.session_state.plan_last_reviewed = None


def load_crisis_plan() -> Dict:
    """Load crisis action plan from file."""
    try:
        if os.path.exists("data/crisis_action_plan.json"):
            with open("data/crisis_action_plan.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load crisis plan: {e}")
    
    # Return empty plan structure
    return {
        "warning_signs": [],
        "internal_coping": [],
        "distraction_activities": [],
        "safe_people": [],
        "safe_places": [],
        "professional_contacts": [],
        "my_therapist": {},
        "reasons_for_living": [],
        "safety_steps": [],
        "emergency_contacts": [],
        "created_date": None,
        "last_updated": None,
        "last_reviewed": None
    }


def save_crisis_plan(plan: Dict) -> bool:
    """Save crisis action plan to file."""
    try:
        os.makedirs("data", exist_ok=True)
        plan["last_updated"] = datetime.now().isoformat()
        with open("data/crisis_action_plan.json", "w") as f:
            json.dump(plan, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save crisis plan: {e}")
        return False


def export_plan_text(plan: Dict) -> str:
    """Export crisis plan as readable text."""
    text = "🆘 MY CRISIS ACTION PLAN\n"
    text += "=" * 60 + "\n\n"
    
    if plan.get('warning_signs'):
        text += "⚠️ WARNING SIGNS TO WATCH FOR:\n"
        for sign in plan['warning_signs']:
            text += f"  • {sign}\n"
        text += "\n"
    
    if plan.get('internal_coping'):
        text += "🧘 INTERNAL COPING STRATEGIES:\n"
        for strategy in plan['internal_coping']:
            text += f"  • {strategy}\n"
        text += "\n"
    
    if plan.get('distraction_activities'):
        text += "🎯 DISTRACTION ACTIVITIES:\n"
        for activity in plan['distraction_activities']:
            text += f"  • {activity}\n"
        text += "\n"
    
    if plan.get('safe_people'):
        text += "👥 PEOPLE I CAN CONTACT:\n"
        for person in plan['safe_people']:
            text += f"  • {person.get('name', 'Unknown')}: {person.get('phone', 'No number')}\n"
            if person.get('notes'):
                text += f"    Note: {person['notes']}\n"
        text += "\n"
    
    if plan.get('safe_places'):
        text += "🏡 SAFE PLACES I CAN GO:\n"
        for place in plan['safe_places']:
            text += f"  • {place}\n"
        text += "\n"
    
    if plan.get('my_therapist'):
        therapist = plan['my_therapist']
        if therapist.get('name'):
            text += "👨‍⚕️ MY THERAPIST:\n"
            text += f"  Name: {therapist.get('name', 'N/A')}\n"
            text += f"  Phone: {therapist.get('phone', 'N/A')}\n"
            if therapist.get('after_hours'):
                text += f"  After Hours: {therapist['after_hours']}\n"
            text += "\n"
    
    text += "🆘 PROFESSIONAL CRISIS RESOURCES:\n"
    text += "  • National Suicide Prevention Lifeline: 988\n"
    text += "  • Crisis Text Line: Text HOME to 741741\n"
    text += "  • Emergency Services: 911\n"
    text += "\n"
    
    if plan.get('reasons_for_living'):
        text += "💝 MY REASONS FOR LIVING:\n"
        for reason in plan['reasons_for_living']:
            text += f"  • {reason}\n"
        text += "\n"
    
    if plan.get('safety_steps'):
        text += "🛡️ SAFETY STEPS:\n"
        for step in plan['safety_steps']:
            text += f"  • {step}\n"
        text += "\n"
    
    text += "=" * 60 + "\n"
    text += f"Last Updated: {plan.get('last_updated', 'Never')}\n"
    
    return text


def render_warning_signs():
    """Render warning signs section."""
    st.markdown("### ⚠️ Step 1: Identify Warning Signs")
    st.info("""
    Recognize the early warning signs that indicate you might be entering a crisis. 
    Being aware of these signs helps you take action early.
    """)
    
    st.markdown("**Select warning signs that apply to you:**")
    
    # Load current selections
    current_signs = st.session_state.crisis_plan.get('warning_signs', [])
    
    # Checkboxes for common signs
    selected_signs = []
    cols = st.columns(2)
    for i, sign in enumerate(COMMON_WARNING_SIGNS):
        with cols[i % 2]:
            if st.checkbox(sign, value=sign in current_signs, key=f"warning_{i}"):
                selected_signs.append(sign)
    
    # Custom warning signs
    st.markdown("**Add your own warning signs:**")
    custom_signs_input = st.text_area(
        "Personal warning signs (one per line):",
        value="\n".join([s for s in current_signs if s not in COMMON_WARNING_SIGNS]),
        height=100,
        key="custom_warning_signs"
    )
    
    if custom_signs_input:
        custom_signs = [s.strip() for s in custom_signs_input.split("\n") if s.strip()]
        selected_signs.extend(custom_signs)
    
    if st.button("💾 Save Warning Signs", use_container_width=True):
        st.session_state.crisis_plan['warning_signs'] = selected_signs
        if not st.session_state.crisis_plan.get('created_date'):
            st.session_state.crisis_plan['created_date'] = datetime.now().isoformat()
        if save_crisis_plan(st.session_state.crisis_plan):
            st.success("✅ Warning signs saved!")


def render_coping_strategies():
    """Render coping strategies section."""
    st.markdown("### 🧘 Step 2: Internal Coping Strategies")
    st.info("""
    Things you can do on your own to calm down and feel better without contacting anyone. 
    These are your first-line strategies when you notice warning signs.
    """)
    
    current_coping = st.session_state.crisis_plan.get('internal_coping', [])
    
    st.markdown("**Select strategies that work for you:**")
    selected_coping = []
    cols = st.columns(2)
    for i, strategy in enumerate(INTERNAL_COPING_STRATEGIES):
        with cols[i % 2]:
            if st.checkbox(strategy, value=strategy in current_coping, key=f"coping_{i}"):
                selected_coping.append(strategy)
    
    st.markdown("**Add your own coping strategies:**")
    custom_coping_input = st.text_area(
        "Personal coping strategies (one per line):",
        value="\n".join([s for s in current_coping if s not in INTERNAL_COPING_STRATEGIES]),
        height=100,
        key="custom_coping"
    )
    
    if custom_coping_input:
        custom_coping = [s.strip() for s in custom_coping_input.split("\n") if s.strip()]
        selected_coping.extend(custom_coping)
    
    if st.button("💾 Save Coping Strategies", use_container_width=True):
        st.session_state.crisis_plan['internal_coping'] = selected_coping
        if save_crisis_plan(st.session_state.crisis_plan):
            st.success("✅ Coping strategies saved!")


def render_distraction_activities():
    """Render distraction activities section."""
    st.markdown("### 🎯 Step 3: Distraction Activities")
    st.info("""
    Activities that can take your mind off the crisis and help you feel better. 
    These involve some level of social contact or engagement with the outside world.
    """)
    
    current_activities = st.session_state.crisis_plan.get('distraction_activities', [])
    
    st.markdown("**Select activities that help you:**")
    selected_activities = []
    cols = st.columns(2)
    for i, activity in enumerate(DISTRACTION_ACTIVITIES):
        with cols[i % 2]:
            if st.checkbox(activity, value=activity in current_activities, key=f"activity_{i}"):
                selected_activities.append(activity)
    
    st.markdown("**Add your own activities:**")
    custom_activities_input = st.text_area(
        "Personal activities (one per line):",
        value="\n".join([s for s in current_activities if s not in DISTRACTION_ACTIVITIES]),
        height=100,
        key="custom_activities"
    )
    
    if custom_activities_input:
        custom_activities = [s.strip() for s in custom_activities_input.split("\n") if s.strip()]
        selected_activities.extend(custom_activities)
    
    if st.button("💾 Save Distraction Activities", use_container_width=True):
        st.session_state.crisis_plan['distraction_activities'] = selected_activities
        if save_crisis_plan(st.session_state.crisis_plan):
            st.success("✅ Distraction activities saved!")


def render_safe_contacts():
    """Render safe people and places section."""
    st.markdown("### 👥 Step 4: People I Can Contact & Safe Places")
    st.info("""
    List trusted people you can reach out to when you're in crisis. Include their phone numbers. 
    Also identify safe places where you can go to feel secure.
    """)
    
    # Safe people
    st.markdown("**Trusted People to Contact:**")
    
    if "temp_safe_people" not in st.session_state:
        st.session_state.temp_safe_people = st.session_state.crisis_plan.get('safe_people', [])
    
    # Add new person
    with st.expander("➕ Add New Contact"):
        with st.form("add_contact_form"):
            col1, col2 = st.columns(2)
            with col1:
                person_name = st.text_input("Name:", placeholder="e.g., Mom, Best Friend Sarah")
                person_phone = st.text_input("Phone Number:", placeholder="e.g., (555) 123-4567")
            with col2:
                person_relationship = st.text_input("Relationship:", placeholder="e.g., Mother, Friend, Sibling")
                person_notes = st.text_input("Notes (optional):", placeholder="e.g., Available after 6 PM")
            
            if st.form_submit_button("Add Contact"):
                if person_name and person_phone:
                    new_contact = {
                        "name": person_name,
                        "phone": person_phone,
                        "relationship": person_relationship,
                        "notes": person_notes
                    }
                    st.session_state.temp_safe_people.append(new_contact)
                    st.session_state.crisis_plan['safe_people'] = st.session_state.temp_safe_people
                    if save_crisis_plan(st.session_state.crisis_plan):
                        st.success(f"✅ Added {person_name}")
                        st.rerun()
    
    # Display current contacts
    if st.session_state.temp_safe_people:
        st.markdown("**Your Contacts:**")
        for i, person in enumerate(st.session_state.temp_safe_people):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"**{person['name']}** ({person.get('relationship', 'N/A')})")
                st.caption(f"📞 {person['phone']}")
                if person.get('notes'):
                    st.caption(f"Note: {person['notes']}")
            with col2:
                if st.button("🗑️", key=f"delete_contact_{i}"):
                    st.session_state.temp_safe_people.pop(i)
                    st.session_state.crisis_plan['safe_people'] = st.session_state.temp_safe_people
                    save_crisis_plan(st.session_state.crisis_plan)
                    st.rerun()
    
    # My therapist/counselor
    st.markdown("---")
    st.markdown("**My Therapist/Counselor:**")
    therapist = st.session_state.crisis_plan.get('my_therapist', {})
    
    col1, col2 = st.columns(2)
    with col1:
        therapist_name = st.text_input("Name:", value=therapist.get('name', ''), key="therapist_name")
        therapist_phone = st.text_input("Phone:", value=therapist.get('phone', ''), key="therapist_phone")
    with col2:
        therapist_after_hours = st.text_input("After Hours/Emergency:", value=therapist.get('after_hours', ''), key="therapist_after_hours")
        therapist_notes = st.text_input("Notes:", value=therapist.get('notes', ''), key="therapist_notes")
    
    if st.button("💾 Save Therapist Info"):
        st.session_state.crisis_plan['my_therapist'] = {
            "name": therapist_name,
            "phone": therapist_phone,
            "after_hours": therapist_after_hours,
            "notes": therapist_notes
        }
        if save_crisis_plan(st.session_state.crisis_plan):
            st.success("✅ Therapist info saved!")
    
    # Safe places
    st.markdown("---")
    st.markdown("**Safe Places I Can Go:**")
    
    current_places = st.session_state.crisis_plan.get('safe_places', [])
    safe_places_input = st.text_area(
        "List safe places (one per line):",
        value="\n".join(current_places),
        placeholder="e.g.,\nLocal library\nFriend's house\n24-hour coffee shop\nPark near my home",
        height=120,
        key="safe_places"
    )
    
    if st.button("💾 Save Safe Places"):
        places = [p.strip() for p in safe_places_input.split("\n") if p.strip()]
        st.session_state.crisis_plan['safe_places'] = places
        if save_crisis_plan(st.session_state.crisis_plan):
            st.success("✅ Safe places saved!")


def render_professional_resources():
    """Render professional resources section."""
    st.markdown("### 🆘 Step 5: Professional Crisis Resources")
    st.info("""
    Keep these professional crisis resources handy. They are available 24/7 and provide 
    free, confidential support when you need immediate help.
    """)
    
    for resource in PROFESSIONAL_RESOURCES:
        with st.expander(f"{resource['name']} - {resource['number']}"):
            st.markdown(f"**Number:** {resource['number']}")
            st.markdown(f"**Available:** {resource['available']}")
            st.markdown(f"**Description:** {resource['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"[Click to call {resource['number']}](tel:{resource['number'].replace(' ', '')})")
            with col2:
                if st.button("📋 Copy Number", key=f"copy_{resource['name']}"):
                    st.code(resource['number'])
    
    st.warning("""
    ⚠️ **If you are in immediate danger or having a medical emergency, call 911 (US) 
    or your local emergency number immediately.**
    """)


def render_reasons_for_living():
    """Render reasons for living section."""
    st.markdown("### 💝 Step 6: My Reasons for Living")
    st.info("""
    These are your personal reasons for staying alive and continuing to fight. 
    They can be people, pets, goals, experiences, or anything meaningful to you.
    During a crisis, these reminders can be life-saving.
    """)
    
    current_reasons = st.session_state.crisis_plan.get('reasons_for_living', [])
    
    st.markdown("**Examples of reasons for living:**")
    st.caption("• My children/family, • My pets, • Future goals or dreams, • People who care about me, • Things I want to experience, • My faith or spirituality, • Making a difference")
    
    reasons_input = st.text_area(
        "My reasons for living (one per line):",
        value="\n".join(current_reasons),
        placeholder="Write your personal reasons...",
        height=200,
        key="reasons_for_living"
    )
    
    if st.button("💾 Save Reasons for Living", use_container_width=True):
        reasons = [r.strip() for r in reasons_input.split("\n") if r.strip()]
        st.session_state.crisis_plan['reasons_for_living'] = reasons
        if save_crisis_plan(st.session_state.crisis_plan):
            st.success("✅ Your reasons for living have been saved!")
            st.balloons()


def render_safety_steps():
    """Render environment safety steps section."""
    st.markdown("### 🛡️ Step 7: Environment Safety Steps")
    st.info("""
    Actions to make your environment safer during a crisis. These steps can help 
    reduce access to means of self-harm and create a supportive space.
    """)
    
    current_steps = st.session_state.crisis_plan.get('safety_steps', [])
    
    st.markdown("**Select safety steps you will take:**")
    selected_steps = []
    for i, step in enumerate(SAFETY_STEPS):
        if st.checkbox(step, value=step in current_steps, key=f"safety_{i}"):
            selected_steps.append(step)
    
    st.markdown("**Additional safety steps:**")
    custom_steps_input = st.text_area(
        "Personal safety steps (one per line):",
        value="\n".join([s for s in current_steps if s not in SAFETY_STEPS]),
        height=100,
        key="custom_safety_steps"
    )
    
    if custom_steps_input:
        custom_steps = [s.strip() for s in custom_steps_input.split("\n") if s.strip()]
        selected_steps.extend(custom_steps)
    
    if st.button("💾 Save Safety Steps", use_container_width=True):
        st.session_state.crisis_plan['safety_steps'] = selected_steps
        if save_crisis_plan(st.session_state.crisis_plan):
            st.success("✅ Safety steps saved!")


def render_view_plan():
    """Render complete crisis plan view."""
    st.markdown("### 📋 My Complete Crisis Action Plan")
    
    plan = st.session_state.crisis_plan
    
    if not plan.get('created_date'):
        st.info("You haven't created a crisis plan yet. Use the builder tabs to create your personalized plan.")
        return
    
    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Export as Text", use_container_width=True):
            plan_text = export_plan_text(plan)
            st.download_button(
                label="💾 Download Plan",
                data=plan_text,
                file_name=f"crisis_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col2:
        if st.button("✅ Mark as Reviewed", use_container_width=True):
            plan['last_reviewed'] = datetime.now().isoformat()
            if save_crisis_plan(plan):
                st.success("Plan marked as reviewed!")
                st.rerun()
    
    with col3:
        if st.button("🔄 Clear Plan", use_container_width=True):
            if st.session_state.get('confirm_clear_plan', False):
                st.session_state.crisis_plan = load_crisis_plan()
                st.session_state.crisis_plan = {
                    "warning_signs": [],
                    "internal_coping": [],
                    "distraction_activities": [],
                    "safe_people": [],
                    "safe_places": [],
                    "professional_contacts": [],
                    "my_therapist": {},
                    "reasons_for_living": [],
                    "safety_steps": [],
                    "emergency_contacts": [],
                    "created_date": None,
                    "last_updated": None,
                    "last_reviewed": None
                }
                save_crisis_plan(st.session_state.crisis_plan)
                st.session_state.confirm_clear_plan = False
                st.success("Plan cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear_plan = True
                st.warning("Click again to confirm clearing the plan.")
    
    # Display plan
    st.markdown("---")
    
    # Plan metadata
    if plan.get('last_updated'):
        last_updated = datetime.fromisoformat(plan['last_updated']).strftime("%B %d, %Y at %I:%M %p")
        st.caption(f"Last updated: {last_updated}")
    if plan.get('last_reviewed'):
        last_reviewed = datetime.fromisoformat(plan['last_reviewed']).strftime("%B %d, %Y")
        st.caption(f"Last reviewed: {last_reviewed}")
    
    st.markdown("---")
    
    # Warning signs
    if plan.get('warning_signs'):
        st.markdown("#### ⚠️ Warning Signs")
        for sign in plan['warning_signs']:
            st.markdown(f"• {sign}")
        st.markdown("---")
    
    # Internal coping
    if plan.get('internal_coping'):
        st.markdown("#### 🧘 Internal Coping Strategies")
        for strategy in plan['internal_coping']:
            st.markdown(f"• {strategy}")
        st.markdown("---")
    
    # Distraction activities
    if plan.get('distraction_activities'):
        st.markdown("#### 🎯 Distraction Activities")
        for activity in plan['distraction_activities']:
            st.markdown(f"• {activity}")
        st.markdown("---")
    
    # Safe people
    if plan.get('safe_people'):
        st.markdown("#### 👥 People I Can Contact")
        for person in plan['safe_people']:
            st.markdown(f"**{person['name']}** ({person.get('relationship', 'N/A')})")
            st.markdown(f"  📞 {person['phone']}")
            if person.get('notes'):
                st.caption(f"  Note: {person['notes']}")
        st.markdown("---")
    
    # Therapist
    if plan.get('my_therapist', {}).get('name'):
        therapist = plan['my_therapist']
        st.markdown("#### 👨‍⚕️ My Therapist/Counselor")
        st.markdown(f"**{therapist['name']}**")
        st.markdown(f"📞 {therapist['phone']}")
        if therapist.get('after_hours'):
            st.markdown(f"🆘 After Hours: {therapist['after_hours']}")
        st.markdown("---")
    
    # Safe places
    if plan.get('safe_places'):
        st.markdown("#### 🏡 Safe Places")
        for place in plan['safe_places']:
            st.markdown(f"• {place}")
        st.markdown("---")
    
    # Professional resources
    st.markdown("#### 🆘 Professional Crisis Resources")
    st.markdown("• **National Suicide Prevention Lifeline:** 988")
    st.markdown("• **Crisis Text Line:** Text HOME to 741741")
    st.markdown("• **Emergency Services:** 911")
    st.markdown("---")
    
    # Reasons for living
    if plan.get('reasons_for_living'):
        st.markdown("#### 💝 My Reasons for Living")
        for reason in plan['reasons_for_living']:
            st.markdown(f"• {reason}")
        st.markdown("---")
    
    # Safety steps
    if plan.get('safety_steps'):
        st.markdown("#### 🛡️ Safety Steps")
        for step in plan['safety_steps']:
            st.markdown(f"• {step}")


def render_crisis_action_plan():
    """Main render function for crisis action plan builder."""
    st.header("🆘 Crisis Action Plan Builder")
    
    # Initialize state
    initialize_crisis_plan_state()
    
    # Critical warning
    st.error("""
    **⚠️ IF YOU ARE IN IMMEDIATE DANGER OR HAVING A MEDICAL EMERGENCY:**
    - Call 911 (US) or your local emergency number
    - Go to the nearest emergency room
    - Call the National Suicide Prevention Lifeline: 988
    - Text HOME to 741741 (Crisis Text Line)
    """)
    
    st.info("""
    💙 Creating a crisis action plan when you're feeling calm can be life-saving when you're in distress. 
    This tool helps you prepare a personalized safety plan with coping strategies, contacts, and resources 
    to use during a mental health crisis.
    """)
    
    # Tab navigation
    tabs = st.tabs([
        "📋 View Plan",
        "⚠️ Warning Signs",
        "🧘 Coping Strategies",
        "🎯 Distractions",
        "👥 Contacts & Places",
        "🆘 Professional Help",
        "💝 Reasons for Living",
        "🛡️ Safety Steps"
    ])
    
    with tabs[0]:
        st.markdown("""
        View your complete crisis action plan. Export it, share it with trusted people, 
        or keep it accessible for when you need it.
        """)
        render_view_plan()
    
    with tabs[1]:
        render_warning_signs()
    
    with tabs[2]:
        render_coping_strategies()
    
    with tabs[3]:
        render_distraction_activities()
    
    with tabs[4]:
        render_safe_contacts()
    
    with tabs[5]:
        render_professional_resources()
    
    with tabs[6]:
        render_reasons_for_living()
    
    with tabs[7]:
        render_safety_steps()
    
    # Reminder at bottom
    st.markdown("---")
    st.warning("""
    **💡 Remember:**
    - Review your crisis plan regularly (monthly recommended)
    - Share it with trusted people (family, friends, therapist)
    - Keep it accessible (saved on phone, printed copy)
    - Update it as your situation changes
    - Practice using your coping strategies before a crisis
    """)
