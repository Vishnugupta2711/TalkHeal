"""
Values Clarification Exercise Component
Interactive questionnaire and ranking tool to help users identify and prioritize
their core personal values. Based on Acceptance and Commitment Therapy (ACT).
Shows alignment between values and current life, suggests value-aligned goals.
"""

import streamlit as st
from datetime import datetime
import json
import os
from typing import Dict, List, Optional
import math

# Core personal values (categorized)
CORE_VALUES = {
    "Relationships": {
        "icon": "❤️",
        "values": [
            {"name": "Family", "description": "Being close to and caring for family members"},
            {"name": "Friendship", "description": "Having close, supportive friendships"},
            {"name": "Intimacy", "description": "Sharing close, loving relationships"},
            {"name": "Community", "description": "Being part of a community or group"},
            {"name": "Marriage/Partnership", "description": "Having a committed romantic relationship"},
            {"name": "Parenting", "description": "Raising and nurturing children"}
        ]
    },
    "Personal Growth": {
        "icon": "🌱",
        "values": [
            {"name": "Learning", "description": "Continuously learning and growing"},
            {"name": "Self-awareness", "description": "Understanding yourself deeply"},
            {"name": "Personal Development", "description": "Becoming your best self"},
            {"name": "Spirituality", "description": "Connecting with something greater"},
            {"name": "Mindfulness", "description": "Living in the present moment"},
            {"name": "Authenticity", "description": "Being true to yourself"}
        ]
    },
    "Work & Achievement": {
        "icon": "💼",
        "values": [
            {"name": "Career Success", "description": "Achieving professional goals"},
            {"name": "Financial Security", "description": "Having stable finances"},
            {"name": "Creativity", "description": "Expressing yourself creatively"},
            {"name": "Achievement", "description": "Accomplishing important goals"},
            {"name": "Recognition", "description": "Being acknowledged for your work"},
            {"name": "Leadership", "description": "Guiding and inspiring others"}
        ]
    },
    "Health & Wellness": {
        "icon": "💪",
        "values": [
            {"name": "Physical Health", "description": "Maintaining a healthy body"},
            {"name": "Mental Health", "description": "Taking care of your mind"},
            {"name": "Fitness", "description": "Being physically active and fit"},
            {"name": "Self-care", "description": "Nurturing and caring for yourself"},
            {"name": "Balance", "description": "Having harmony in life"},
            {"name": "Peace", "description": "Living with inner calm"}
        ]
    },
    "Recreation & Pleasure": {
        "icon": "🎨",
        "values": [
            {"name": "Fun", "description": "Enjoying life and having a good time"},
            {"name": "Adventure", "description": "Seeking new experiences"},
            {"name": "Travel", "description": "Exploring new places"},
            {"name": "Hobbies", "description": "Pursuing interests and passions"},
            {"name": "Relaxation", "description": "Taking time to rest and recharge"},
            {"name": "Beauty", "description": "Appreciating and creating beauty"}
        ]
    },
    "Contribution": {
        "icon": "🌍",
        "values": [
            {"name": "Helping Others", "description": "Making a positive impact"},
            {"name": "Justice", "description": "Fighting for what's right"},
            {"name": "Environmental Care", "description": "Protecting the planet"},
            {"name": "Compassion", "description": "Being kind and empathetic"},
            {"name": "Generosity", "description": "Giving to others freely"},
            {"name": "Service", "description": "Contributing to society"}
        ]
    },
    "Character": {
        "icon": "⭐",
        "values": [
            {"name": "Honesty", "description": "Being truthful and genuine"},
            {"name": "Courage", "description": "Facing fears and challenges"},
            {"name": "Independence", "description": "Being self-reliant"},
            {"name": "Responsibility", "description": "Being accountable"},
            {"name": "Loyalty", "description": "Being faithful and committed"},
            {"name": "Humility", "description": "Being modest and grounded"}
        ]
    }
}

# Reflection questions for each life area
LIFE_AREAS = {
    "Work/Career": "How do you want to be in your work? What kind of worker do you want to be?",
    "Relationships": "What kind of relationships do you want? How do you want to treat others?",
    "Personal Growth": "What kind of person do you want to become? How do you want to grow?",
    "Health": "How do you want to care for your physical and mental health?",
    "Leisure": "How do you want to enjoy your free time? What brings you joy?",
    "Community": "How do you want to contribute to your community or world?"
}


def initialize_values_state():
    """Initialize session state for values clarification."""
    if "values_assessment" not in st.session_state:
        st.session_state.values_assessment = load_values_assessment()
    if "selected_values" not in st.session_state:
        st.session_state.selected_values = []
    if "values_ranking" not in st.session_state:
        st.session_state.values_ranking = []
    if "values_alignment" not in st.session_state:
        st.session_state.values_alignment = {}


def load_values_assessment() -> Dict:
    """Load values assessment from file."""
    try:
        if os.path.exists("data/values_assessment.json"):
            with open("data/values_assessment.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load values assessment: {e}")
    return {
        "selected_values": [],
        "ranked_values": [],
        "alignment_scores": {},
        "goals": [],
        "created_date": None,
        "last_updated": None
    }


def save_values_assessment(assessment: Dict) -> bool:
    """Save values assessment to file."""
    try:
        os.makedirs("data", exist_ok=True)
        assessment["last_updated"] = datetime.now().isoformat()
        with open("data/values_assessment.json", "w") as f:
            json.dump(assessment, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save values assessment: {e}")
        return False


def render_values_identification():
    """Render values identification step."""
    st.markdown("### 🎯 Step 1: Identify Your Values")
    st.info("""
    Review the values below and select the ones that resonate with you. Choose values that 
    represent what's truly important to you, not what you think should be important.
    """)
    
    st.markdown("**Select 10-15 values that matter most to you:**")
    
    selected_values = []
    
    for category, data in CORE_VALUES.items():
        with st.expander(f"{data['icon']} {category} ({len(data['values'])} values)"):
            cols = st.columns(2)
            for i, value in enumerate(data['values']):
                with cols[i % 2]:
                    checked = st.checkbox(
                        f"**{value['name']}**",
                        key=f"value_{category}_{value['name']}",
                        help=value['description']
                    )
                    st.caption(value['description'])
                    
                    if checked:
                        selected_values.append({
                            "name": value['name'],
                            "category": category,
                            "description": value['description']
                        })
    
    st.markdown("---")
    st.markdown(f"**Selected: {len(selected_values)} values**")
    
    if len(selected_values) < 5:
        st.warning("Select at least 5 values to continue.")
    elif len(selected_values) > 20:
        st.warning("Consider narrowing down to 10-15 most important values.")
    else:
        st.success(f"✓ You've selected {len(selected_values)} values - great!")
    
    if st.button("💾 Save & Continue to Ranking", use_container_width=True, type="primary"):
        if len(selected_values) < 5:
            st.error("Please select at least 5 values before continuing.")
        else:
            st.session_state.values_assessment["selected_values"] = selected_values
            if not st.session_state.values_assessment.get("created_date"):
                st.session_state.values_assessment["created_date"] = datetime.now().isoformat()
            if save_values_assessment(st.session_state.values_assessment):
                st.success("✅ Values saved! Go to the Ranking tab to prioritize them.")


def render_values_ranking():
    """Render values ranking step."""
    st.markdown("### 📊 Step 2: Rank Your Values")
    
    selected_values = st.session_state.values_assessment.get("selected_values", [])
    
    if not selected_values:
        st.info("Please complete Step 1 (Identify Values) first.")
        return
    
    st.info(f"""
    Now prioritize your {len(selected_values)} selected values. Drag and drop or use the ranking 
    buttons to order them from most important (top) to least important (bottom).
    """)
    
    st.markdown("**Your Values (in order of importance):**")
    
    # Get current ranking or initialize
    if "temp_ranking" not in st.session_state:
        # Check if there's a saved ranking
        saved_ranking = st.session_state.values_assessment.get("ranked_values", [])
        if saved_ranking:
            st.session_state.temp_ranking = saved_ranking
        else:
            st.session_state.temp_ranking = selected_values.copy()
    
    ranking = st.session_state.temp_ranking
    
    # Display ranked values with move buttons
    for i, value in enumerate(ranking):
        col1, col2, col3, col4 = st.columns([0.1, 0.6, 0.15, 0.15])
        
        with col1:
            st.markdown(f"**{i+1}.**")
        
        with col2:
            st.markdown(f"**{value['name']}** ({value['category']})")
            st.caption(value['description'])
        
        with col3:
            if i > 0:
                if st.button("⬆️", key=f"up_{i}"):
                    # Move up
                    ranking[i], ranking[i-1] = ranking[i-1], ranking[i]
                    st.session_state.temp_ranking = ranking
                    st.rerun()
        
        with col4:
            if i < len(ranking) - 1:
                if st.button("⬇️", key=f"down_{i}"):
                    # Move down
                    ranking[i], ranking[i+1] = ranking[i+1], ranking[i]
                    st.session_state.temp_ranking = ranking
                    st.rerun()
    
    st.markdown("---")
    
    # Save ranking
    if st.button("💾 Save Ranking", use_container_width=True, type="primary"):
        st.session_state.values_assessment["ranked_values"] = ranking
        if save_values_assessment(st.session_state.values_assessment):
            st.success("✅ Value ranking saved! Go to Alignment tab to assess your current life.")
            st.balloons()


def render_values_alignment():
    """Render values alignment assessment."""
    st.markdown("### ⚖️ Step 3: Values Alignment Assessment")
    
    ranked_values = st.session_state.values_assessment.get("ranked_values", [])
    
    if not ranked_values:
        st.info("Please complete Steps 1 & 2 first (Identify and Rank values).")
        return
    
    st.info("""
    For each of your top values, rate how well your current life aligns with that value. 
    This helps identify gaps between what matters to you and how you're living.
    """)
    
    st.markdown("**Rate your alignment (1 = Not aligned at all, 10 = Perfectly aligned):**")
    
    alignment_scores = st.session_state.values_assessment.get("alignment_scores", {})
    
    # Focus on top 10 values
    top_values = ranked_values[:10]
    
    for i, value in enumerate(top_values, 1):
        st.markdown(f"**{i}. {value['name']}** - {value['description']}")
        
        current_score = alignment_scores.get(value['name'], 5)
        
        score = st.slider(
            f"Current alignment with {value['name']}:",
            min_value=1,
            max_value=10,
            value=current_score,
            key=f"align_{value['name']}",
            help="1 = Not living according to this value, 10 = Fully living this value"
        )
        
        alignment_scores[value['name']] = score
        
        # Color-coded feedback
        if score >= 8:
            st.success(f"✓ Strong alignment with {value['name']}")
        elif score >= 5:
            st.info(f"↔ Moderate alignment with {value['name']}")
        else:
            st.warning(f"⚠ Low alignment with {value['name']} - opportunity for growth")
        
        st.markdown("---")
    
    if st.button("💾 Save Alignment Assessment", use_container_width=True, type="primary"):
        st.session_state.values_assessment["alignment_scores"] = alignment_scores
        if save_values_assessment(st.session_state.values_assessment):
            st.success("✅ Alignment assessment saved! View your results in the Results tab.")


def render_visual_results():
    """Render visual representation of values and alignment."""
    st.markdown("### 📊 Your Values Profile")
    
    ranked_values = st.session_state.values_assessment.get("ranked_values", [])
    alignment_scores = st.session_state.values_assessment.get("alignment_scores", {})
    
    if not ranked_values:
        st.info("Complete the values identification and ranking process to see your profile.")
        return
    
    # Top values display
    st.markdown("#### 🏆 Your Top 5 Values")
    
    top_5 = ranked_values[:5]
    
    for i, value in enumerate(top_5, 1):
        col1, col2 = st.columns([0.7, 0.3])
        
        with col1:
            st.markdown(f"**{i}. {value['name']}**")
            st.caption(value['description'])
        
        with col2:
            alignment = alignment_scores.get(value['name'], 0)
            if alignment > 0:
                st.metric("Alignment", f"{alignment}/10")
    
    # Values by category
    st.markdown("---")
    st.markdown("#### 📋 Values by Category")
    
    category_counts = {}
    for value in ranked_values:
        cat = value['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for category in CORE_VALUES.keys():
        if category in category_counts:
            count = category_counts[category]
            icon = CORE_VALUES[category]['icon']
            st.write(f"{icon} **{category}:** {count} values")
    
    # Alignment analysis
    if alignment_scores:
        st.markdown("---")
        st.markdown("#### ⚖️ Alignment Analysis")
        
        # Calculate average alignment
        scores = list(alignment_scores.values())
        avg_alignment = sum(scores) / len(scores) if scores else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Alignment", f"{avg_alignment:.1f}/10")
        
        with col2:
            high_alignment = sum(1 for s in scores if s >= 8)
            st.metric("High Alignment", f"{high_alignment} values")
        
        with col3:
            low_alignment = sum(1 for s in scores if s < 5)
            st.metric("Needs Attention", f"{low_alignment} values")
        
        # Gap analysis
        st.markdown("#### 🎯 Values Gaps (Opportunities for Growth)")
        
        gaps = []
        for value in ranked_values[:10]:
            score = alignment_scores.get(value['name'], 0)
            if score < 7:
                gap = 10 - score
                gaps.append({
                    "value": value['name'],
                    "score": score,
                    "gap": gap,
                    "rank": ranked_values.index(value) + 1
                })
        
        if gaps:
            # Sort by importance (rank) and gap size
            gaps.sort(key=lambda x: (x['rank'], -x['gap']))
            
            for gap_info in gaps[:5]:
                st.warning(f"""
                **{gap_info['value']}** (Rank #{gap_info['rank']})  
                Current alignment: {gap_info['score']}/10  
                Gap: {gap_info['gap']} points
                """)
        else:
            st.success("✨ Great alignment! You're living according to your values.")


def render_action_plan():
    """Render action plan based on values."""
    st.markdown("### 🎯 Value-Aligned Action Plan")
    
    ranked_values = st.session_state.values_assessment.get("ranked_values", [])
    alignment_scores = st.session_state.values_assessment.get("alignment_scores", {})
    
    if not ranked_values or not alignment_scores:
        st.info("Complete the alignment assessment to generate your action plan.")
        return
    
    st.info("""
    Based on your values and alignment assessment, here are suggested actions to live 
    more in line with what matters most to you.
    """)
    
    # Identify values needing attention
    action_values = []
    for value in ranked_values[:10]:
        score = alignment_scores.get(value['name'], 0)
        if score < 7:
            action_values.append({
                "name": value['name'],
                "description": value['description'],
                "category": value['category'],
                "score": score,
                "rank": ranked_values.index(value) + 1
            })
    
    if not action_values:
        st.success("🎉 You're living well-aligned with your values! Keep it up!")
        return
    
    st.markdown(f"**Focus on these {len(action_values)} value(s):**")
    
    for value_info in action_values:
        with st.expander(f"💡 Actions for: {value_info['name']} (Current: {value_info['score']}/10)"):
            st.markdown(f"**Value Description:** {value_info['description']}")
            st.markdown(f"**Category:** {value_info['category']}")
            st.markdown(f"**Your Ranking:** #{value_info['rank']}")
            
            st.markdown("**Reflection Questions:**")
            st.markdown(f"""
            - What would it look like to live more in line with {value_info['name']}?
            - What small step could you take this week to honor this value?
            - What obstacles prevent you from living this value more fully?
            - Who could support you in living this value?
            """)
            
            # Goal setting
            st.markdown("**Set a Goal:**")
            goal_input = st.text_area(
                f"My goal for {value_info['name']}:",
                placeholder=f"e.g., Spend 30 minutes daily on activities related to {value_info['name']}",
                key=f"goal_{value_info['name']}"
            )
            
            if goal_input:
                if st.button(f"💾 Save Goal for {value_info['name']}", key=f"save_goal_{value_info['name']}"):
                    goals = st.session_state.values_assessment.get("goals", [])
                    goals.append({
                        "value": value_info['name'],
                        "goal": goal_input,
                        "date": datetime.now().isoformat()
                    })
                    st.session_state.values_assessment["goals"] = goals
                    if save_values_assessment(st.session_state.values_assessment):
                        st.success(f"✅ Goal saved for {value_info['name']}!")
    
    # Display saved goals
    saved_goals = st.session_state.values_assessment.get("goals", [])
    if saved_goals:
        st.markdown("---")
        st.markdown("### 📝 Your Value-Aligned Goals")
        
        for goal in saved_goals[-5:]:  # Show last 5 goals
            st.success(f"""
            **{goal['value']}**  
            {goal['goal']}  
            *Set on: {datetime.fromisoformat(goal['date']).strftime('%B %d, %Y')}*
            """)


def render_education():
    """Render educational content about values clarification."""
    st.markdown("### 📚 Understanding Values Clarification")
    
    st.info("""
    **Values** are chosen life directions - what you want to stand for, how you want to behave, 
    what sort of person you want to be, and what is truly important and meaningful to you.
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Why Values Matter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Benefits of Living by Values:**")
        st.success("""
        • **Direction:** Values guide decisions
        • **Meaning:** Creates sense of purpose
        • **Motivation:** Inspires action
        • **Fulfillment:** Increases life satisfaction
        • **Resilience:** Helps through difficult times
        • **Authenticity:** Be true to yourself
        • **Reduced regret:** Make choices you're proud of
        """)
    
    with col2:
        st.markdown("**Values vs. Goals:**")
        st.info("""
        **Values** are ongoing directions (like "heading west")
        - Never fully "achieved"
        - Always available to live by
        - Example: Being a loving parent
        
        **Goals** are specific achievements
        - Can be completed
        - Milestone markers
        - Example: Attend child's recital
        
        Goals serve values!
        """)
    
    st.markdown("---")
    st.markdown("### 🧠 Values in ACT (Acceptance and Commitment Therapy)")
    
    st.markdown("""
    Values clarification is a core component of **Acceptance and Commitment Therapy (ACT)**, 
    an evidence-based approach that helps people live more meaningful lives.
    
    **The ACT approach to values:**
    1. **Clarify** what truly matters to you
    2. **Notice** when you're off track
    3. **Choose** actions aligned with values
    4. **Accept** discomfort in service of values
    5. **Commit** to value-guided living
    
    **Key principles:**
    - Values are **chosen**, not imposed
    - Values are about **how** you want to behave
    - Values guide **moment-to-moment** choices
    - You can live your values **right now**
    - Values don't depend on external outcomes
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Common Values Challenges")
    
    st.warning("""
    **Living by values can be difficult when:**
    - **Conflicting values:** Two values seem incompatible (e.g., adventure vs. security)
      - *Solution:* Find ways to honor both; it's about balance, not all-or-nothing
    
    - **Others' expectations:** Living others' values instead of your own
      - *Solution:* Reflect on what YOU truly care about, not what you "should" care about
    
    - **Old habits:** Automatic behaviors don't align with values
      - *Solution:* Use awareness to catch yourself and make conscious choices
    
    - **Fear and discomfort:** Values-aligned action feels scary
      - *Solution:* Courage means acting on values despite fear
    
    - **Perfectionism:** Waiting for perfect conditions
      - *Solution:* Take small steps; perfect alignment isn't required
    """)
    
    st.markdown("---")
    st.markdown("### 🔄 Using This Tool Regularly")
    
    st.markdown("""
    **Recommended practice:**
    - **Initial assessment:** Complete all steps thoroughly
    - **Monthly review:** Check alignment scores
    - **Quarterly re-ranking:** Values can shift over time
    - **Annual deep dive:** Reassess and set new goals
    
    **Daily application:**
    - Morning: Review top 3 values
    - Throughout day: Ask "Is this choice aligned with my values?"
    - Evening: Reflect on how you lived your values today
    
    **Decision-making with values:**
    1. Face a decision
    2. Ask "Which option better aligns with my values?"
    3. Consider both short-term and long-term alignment
    4. Make the choice that serves your values
    5. Accept any discomfort that comes with the value-aligned choice
    """)
    
    st.markdown("---")
    st.markdown("### 📖 Additional Resources")
    
    st.markdown("""
    **Books:**
    - "The Happiness Trap" by Russ Harris (ACT and values)
    - "Get Out of Your Mind and Into Your Life" by Steven Hayes
    - "The Confidence Gap" by Russ Harris
    
    **Websites:**
    - [ACT Mindfully](https://www.actmindfully.com.au) - Free values resources
    - [Association for Contextual Behavioral Science](https://contextualscience.org)
    
    **Research:**
    - Values clarification shown to increase well-being
    - Values-based living reduces anxiety and depression
    - Key component of evidence-based ACT therapy
    """)


def render_values_clarification():
    """Main render function for values clarification exercise."""
    st.header("🎯 Values Clarification Exercise")
    
    # Initialize state
    initialize_values_state()
    
    st.info("""
    💝 Discover what truly matters to you! This exercise helps you identify your core personal values, 
    prioritize them, and assess how well your current life aligns with these values. Based on 
    Acceptance and Commitment Therapy (ACT), this process provides direction and meaning for your life.
    """)
    
    # Tab navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 1. Identify",
        "📊 2. Rank",
        "⚖️ 3. Alignment",
        "📈 Results",
        "🎯 Action Plan",
        "📚 Learn"
    ])
    
    with tab1:
        st.markdown("""
        Explore different life values and select the ones that resonate with you. 
        Choose what truly matters to YOU, not what you think should matter.
        """)
        render_values_identification()
    
    with tab2:
        st.markdown("""
        Prioritize your selected values from most to least important. This helps clarify 
        what matters most when facing difficult decisions.
        """)
        render_values_ranking()
    
    with tab3:
        st.markdown("""
        Rate how well your current life aligns with each value. This reveals gaps between 
        what matters to you and how you're actually living.
        """)
        render_values_alignment()
    
    with tab4:
        st.markdown("""
        View your values profile, top priorities, and alignment analysis. See where you're 
        living in harmony with your values and where there are opportunities for growth.
        """)
        render_visual_results()
    
    with tab5:
        st.markdown("""
        Create an action plan to live more in alignment with your values. Set goals and 
        take steps toward a more meaningful life.
        """)
        render_action_plan()
    
    with tab6:
        render_education()
    
    # Quick reminder at bottom
    st.markdown("---")
    st.success("""
    💡 **Remember:** Values are like a compass - they show the direction, but you choose each step. 
    You can always take one small action today that aligns with your values.
    """)
