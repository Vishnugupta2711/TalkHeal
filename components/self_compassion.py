"""
Self-Compassion Practice Tool Component
Guided exercises based on Dr. Kristin Neff's self-compassion framework.
Includes self-compassion breaks, compassionate letter writing, comparison exercises,
and journaling with educational content about the three components of self-compassion.
"""

import streamlit as st
from datetime import datetime, date
import json
import os
from typing import Dict, List, Optional

# Self-compassion framework components
SELF_COMPASSION_COMPONENTS = {
    "Self-Kindness": {
        "icon": "💝",
        "description": "Being warm and understanding toward ourselves when we suffer, fail, or feel inadequate, rather than ignoring our pain or flagellating ourselves with self-criticism.",
        "practices": [
            "Speak to yourself as you would to a good friend",
            "Acknowledge that suffering is part of being human",
            "Treat mistakes as opportunities to grow",
            "Use gentle, supportive self-talk",
            "Allow yourself to be imperfect"
        ]
    },
    "Common Humanity": {
        "icon": "🌍",
        "description": "Recognizing that suffering and personal inadequacy are part of the shared human experience – something we all go through rather than something that happens to 'me' alone.",
        "practices": [
            "Remember that everyone struggles",
            "Connect struggles to universal human experience",
            "Recognize you're not alone in your feelings",
            "See imperfection as part of being human",
            "Feel connected rather than isolated"
        ]
    },
    "Mindfulness": {
        "icon": "🧘‍♀️",
        "description": "Taking a balanced approach to negative emotions so that feelings are neither suppressed nor exaggerated. We observe our thoughts and feelings without over-identifying with them.",
        "practices": [
            "Observe thoughts without judgment",
            "Hold painful feelings with awareness",
            "Avoid over-identification with emotions",
            "Balance acceptance with action",
            "Stay present with difficult experiences"
        ]
    }
}

# Daily prompts for self-compassion practice
DAILY_PROMPTS = [
    "What is one kind thing I can do for myself today?",
    "How am I being hard on myself right now? How can I respond with kindness?",
    "What would I say to a friend in my situation?",
    "How is my struggle connected to the larger human experience?",
    "What do I need right now to feel supported and cared for?",
    "What difficult emotion am I experiencing? Can I hold it with kindness?",
    "How can I acknowledge my pain without exaggerating or minimizing it?",
    "What part of me needs compassion right now?",
    "How can I be a good friend to myself today?",
    "What am I grateful for about myself, even with my imperfections?"
]

# Self-compassion break phrases (Dr. Kristin Neff)
COMPASSION_BREAK_PHRASES = {
    "Mindfulness": [
        "This is a moment of suffering.",
        "This is difficult right now.",
        "This hurts.",
        "This is stressful.",
        "I'm struggling right now."
    ],
    "Common Humanity": [
        "Suffering is a part of life.",
        "Everyone struggles sometimes.",
        "I'm not alone in this.",
        "Others feel this way too.",
        "This is part of being human."
    ],
    "Self-Kindness": [
        "May I be kind to myself.",
        "May I give myself the compassion I need.",
        "May I accept myself as I am.",
        "May I be patient with myself.",
        "May I be gentle with myself."
    ]
}

# Self-criticism vs self-compassion comparison prompts
COMPARISON_PROMPTS = [
    {
        "situation": "Making a mistake at work",
        "self_critical": "I'm so stupid. I always mess things up. I'm incompetent.",
        "self_compassionate": "I made a mistake. Everyone makes mistakes sometimes. I can learn from this and do better next time. This doesn't define me."
    },
    {
        "situation": "Not meeting a personal goal",
        "self_critical": "I'm a failure. I have no willpower. I'll never achieve anything.",
        "self_compassionate": "I didn't reach my goal this time, and that's disappointing. Many people struggle with this. I can adjust my approach and try again with kindness."
    },
    {
        "situation": "Feeling socially awkward",
        "self_critical": "I'm so weird. Nobody likes me. I always say the wrong thing.",
        "self_compassionate": "I felt uncomfortable in that social situation. Social anxiety is common. I'm doing my best, and that's okay."
    },
    {
        "situation": "Body image concerns",
        "self_critical": "I'm ugly. My body is disgusting. I hate how I look.",
        "self_compassionate": "I'm struggling with how I look right now. Many people have body image concerns. I deserve kindness regardless of my appearance."
    }
]


def initialize_compassion_state():
    """Initialize session state for self-compassion tool."""
    if "compassion_journal" not in st.session_state:
        st.session_state.compassion_journal = load_compassion_journal()
    if "compassion_letters" not in st.session_state:
        st.session_state.compassion_letters = load_compassion_letters()
    if "compassion_practices" not in st.session_state:
        st.session_state.compassion_practices = load_compassion_practices()
    if "daily_prompt_index" not in st.session_state:
        st.session_state.daily_prompt_index = datetime.now().day % len(DAILY_PROMPTS)


def load_compassion_journal() -> List[Dict]:
    """Load self-compassion journal entries."""
    try:
        if os.path.exists("data/compassion_journal.json"):
            with open("data/compassion_journal.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load journal: {e}")
    return []


def save_compassion_journal(journal: List[Dict]) -> bool:
    """Save self-compassion journal entries."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/compassion_journal.json", "w") as f:
            json.dump(journal, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save journal: {e}")
        return False


def load_compassion_letters() -> List[Dict]:
    """Load compassionate letters."""
    try:
        if os.path.exists("data/compassion_letters.json"):
            with open("data/compassion_letters.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load letters: {e}")
    return []


def save_compassion_letters(letters: List[Dict]) -> bool:
    """Save compassionate letters."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/compassion_letters.json", "w") as f:
            json.dump(letters, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save letters: {e}")
        return False


def load_compassion_practices() -> List[Dict]:
    """Load practice records."""
    try:
        if os.path.exists("data/compassion_practices.json"):
            with open("data/compassion_practices.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load practices: {e}")
    return []


def save_compassion_practices(practices: List[Dict]) -> bool:
    """Save practice records."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/compassion_practices.json", "w") as f:
            json.dump(practices, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Could not save practices: {e}")
        return False


def render_compassion_break():
    """Render self-compassion break exercise."""
    st.markdown("### 🫂 Self-Compassion Break")
    st.info("""
    The Self-Compassion Break is a quick practice you can use anytime you're struggling. 
    It involves three steps based on the three components of self-compassion.
    """)
    
    st.markdown("#### How to Practice:")
    
    # Step 1: Mindfulness
    st.markdown("**Step 1: Mindfulness** 🧘‍♀️")
    st.caption("Acknowledge that this is a difficult moment")
    
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        selected_mindfulness = st.radio(
            "Choose a phrase or write your own:",
            options=COMPASSION_BREAK_PHRASES["Mindfulness"] + ["Custom..."],
            key="mindfulness_phrase"
        )
    
    if selected_mindfulness == "Custom...":
        custom_mindfulness = st.text_input(
            "Your mindfulness statement:",
            placeholder="Describe what you're experiencing...",
            key="custom_mindfulness"
        )
        if custom_mindfulness:
            selected_mindfulness = custom_mindfulness
    
    # Step 2: Common Humanity
    st.markdown("**Step 2: Common Humanity** 🌍")
    st.caption("Remember that you're not alone in this struggle")
    
    selected_humanity = st.radio(
        "Choose a phrase or write your own:",
        options=COMPASSION_BREAK_PHRASES["Common Humanity"] + ["Custom..."],
        key="humanity_phrase"
    )
    
    if selected_humanity == "Custom...":
        custom_humanity = st.text_input(
            "Your common humanity statement:",
            placeholder="Connect your experience to others...",
            key="custom_humanity"
        )
        if custom_humanity:
            selected_humanity = custom_humanity
    
    # Step 3: Self-Kindness
    st.markdown("**Step 3: Self-Kindness** 💝")
    st.caption("Offer yourself kindness and care")
    
    selected_kindness = st.radio(
        "Choose a phrase or write your own:",
        options=COMPASSION_BREAK_PHRASES["Self-Kindness"] + ["Custom..."],
        key="kindness_phrase"
    )
    
    if selected_kindness == "Custom...":
        custom_kindness = st.text_input(
            "Your self-kindness statement:",
            placeholder="What kindness do you need right now?",
            key="custom_kindness"
        )
        if custom_kindness:
            selected_kindness = custom_kindness
    
    # Practice together
    st.markdown("---")
    st.markdown("### 🎯 Your Self-Compassion Break")
    
    if st.button("🧘‍♀️ Practice Now", use_container_width=True, type="primary"):
        st.markdown("""
        <div style='background-color: rgba(255, 182, 193, 0.1); padding: 20px; border-radius: 10px; margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**🧘‍♀️ Mindfulness:**")
        st.markdown(f"*{selected_mindfulness}*")
        st.markdown("")
        
        st.markdown(f"**🌍 Common Humanity:**")
        st.markdown(f"*{selected_humanity}*")
        st.markdown("")
        
        st.markdown(f"**💝 Self-Kindness:**")
        st.markdown(f"*{selected_kindness}*")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.success("✨ Take a few deep breaths and let these words sink in.")
        
        # Optional: Save practice
        if st.button("💾 Save This Practice"):
            practice_entry = {
                "type": "Self-Compassion Break",
                "date": datetime.now().isoformat(),
                "mindfulness": selected_mindfulness,
                "common_humanity": selected_humanity,
                "self_kindness": selected_kindness,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.compassion_practices.append(practice_entry)
            if save_compassion_practices(st.session_state.compassion_practices):
                st.success("✅ Practice saved!")
                st.balloons()


def render_compassionate_letter():
    """Render compassionate letter writing exercise."""
    st.markdown("### 💌 Compassionate Letter to Yourself")
    st.info("""
    Writing a compassionate letter to yourself can be a powerful way to develop self-kindness. 
    Imagine you're writing to a dear friend who is struggling with what you're going through.
    """)
    
    st.markdown("#### Guidance for Your Letter:")
    
    with st.expander("📖 Tips for Writing a Compassionate Letter"):
        st.markdown("""
        **What to include:**
        - Acknowledge the difficulty you're facing
        - Express understanding and validation
        - Remind yourself that struggle is part of being human
        - Offer words of kindness and encouragement
        - Suggest self-care or support you might need
        
        **Tone to use:**
        - Warm and caring (as you'd speak to a friend)
        - Non-judgmental and accepting
        - Gentle and supportive
        - Hopeful but realistic
        
        **What to avoid:**
        - Harsh criticism or "tough love"
        - Minimizing your feelings
        - Comparing yourself to others negatively
        - Perfectionist demands
        """)
    
    with st.form("compassionate_letter_form"):
        st.markdown("**What are you struggling with?**")
        struggle = st.text_area(
            "Your situation:",
            placeholder="Describe what's been difficult for you...",
            height=100,
            key="letter_struggle"
        )
        
        st.markdown("**Write Your Compassionate Letter**")
        st.caption("Dear [Your Name],")
        
        letter_content = st.text_area(
            "Your letter:",
            placeholder="I know you're going through a difficult time right now...",
            height=300,
            key="letter_content"
        )
        
        st.caption("With compassion, [Your Name]")
        
        col1, col2 = st.columns(2)
        with col1:
            save_letter = st.form_submit_button("💾 Save Letter", use_container_width=True)
        with col2:
            preview_letter = st.form_submit_button("👁️ Preview Letter", use_container_width=True)
        
        if save_letter and letter_content:
            letter_entry = {
                "struggle": struggle,
                "letter": letter_content,
                "date": datetime.now().isoformat(),
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.compassion_letters.append(letter_entry)
            if save_compassion_letters(st.session_state.compassion_letters):
                st.success("✅ Your compassionate letter has been saved!")
                st.balloons()
        
        if preview_letter and letter_content:
            st.markdown("---")
            st.markdown("### 📬 Your Letter")
            st.markdown(f"""
            <div style='background-color: rgba(255, 255, 224, 0.3); padding: 20px; border-radius: 10px; border-left: 4px solid #FFD700;'>
            <p><strong>Dear Self,</strong></p>
            <p>{letter_content.replace(chr(10), '</p><p>')}</p>
            <p><strong>With compassion,</strong></p>
            <p><strong>Me</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show saved letters
    if st.session_state.compassion_letters:
        st.markdown("---")
        st.markdown("### 📚 Your Compassionate Letters")
        
        for i, letter in enumerate(reversed(st.session_state.compassion_letters[-5:])):
            date_str = datetime.fromisoformat(letter['date']).strftime("%B %d, %Y")
            with st.expander(f"💌 Letter from {date_str}"):
                if letter.get('struggle'):
                    st.markdown(f"**Struggling with:** {letter['struggle']}")
                    st.markdown("---")
                st.markdown(letter['letter'])


def render_criticism_comparison():
    """Render self-criticism vs self-compassion comparison exercise."""
    st.markdown("### ⚖️ Self-Criticism vs Self-Compassion")
    st.info("""
    This exercise helps you recognize the difference between self-criticism and self-compassion. 
    By comparing these approaches, you can learn to respond to yourself with more kindness.
    """)
    
    # Show examples
    st.markdown("#### 📖 Examples to Learn From")
    
    for i, example in enumerate(COMPARISON_PROMPTS):
        with st.expander(f"Example {i+1}: {example['situation']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**❌ Self-Critical Response:**")
                st.error(example['self_critical'])
            
            with col2:
                st.markdown("**✅ Self-Compassionate Response:**")
                st.success(example['self_compassionate'])
    
    # Practice with own situation
    st.markdown("---")
    st.markdown("#### ✍️ Practice With Your Own Situation")
    
    with st.form("comparison_form"):
        situation = st.text_input(
            "**Describe a situation where you're being self-critical:**",
            placeholder="e.g., I forgot an important appointment...",
            key="comparison_situation"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**❌ Your Self-Critical Thoughts:**")
            self_critical = st.text_area(
                "What harsh things are you saying to yourself?",
                placeholder="Write your self-critical thoughts...",
                height=150,
                key="self_critical_thoughts"
            )
        
        with col2:
            st.markdown("**✅ Reframe with Self-Compassion:**")
            st.caption("Use the three components: mindfulness, common humanity, self-kindness")
            self_compassionate = st.text_area(
                "How can you respond with compassion?",
                placeholder="Write a self-compassionate response...",
                height=150,
                key="self_compassionate_thoughts"
            )
        
        submitted = st.form_submit_button("💾 Save Comparison", use_container_width=True)
        
        if submitted and situation and self_critical and self_compassionate:
            comparison_entry = {
                "type": "Criticism Comparison",
                "situation": situation,
                "self_critical": self_critical,
                "self_compassionate": self_compassionate,
                "date": datetime.now().isoformat(),
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.compassion_practices.append(comparison_entry)
            if save_compassion_practices(st.session_state.compassion_practices):
                st.success("✅ Comparison saved! Notice how different these responses feel.")
                st.balloons()


def render_compassion_journal():
    """Render self-compassion journal."""
    st.markdown("### 📓 Self-Compassion Journal")
    
    # Daily prompt
    st.markdown("#### 🌟 Today's Prompt")
    prompt = DAILY_PROMPTS[st.session_state.daily_prompt_index]
    st.info(f"**{prompt}**")
    
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("🔄 New Prompt"):
            st.session_state.daily_prompt_index = (st.session_state.daily_prompt_index + 1) % len(DAILY_PROMPTS)
            st.rerun()
    
    # Journal entry form
    with st.form("journal_form"):
        entry_date = st.date_input(
            "Date:",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )
        
        journal_entry = st.text_area(
            "Your reflection:",
            placeholder="Take a moment to reflect with self-compassion...",
            height=200,
            key="journal_entry"
        )
        
        # Mood/feeling selector
        feelings = st.multiselect(
            "How are you feeling?",
            options=[
                "Peaceful", "Calm", "Hopeful", "Grateful", "Sad",
                "Anxious", "Frustrated", "Tired", "Confused", "Overwhelmed"
            ],
            key="journal_feelings"
        )
        
        submitted = st.form_submit_button("💾 Save Entry", use_container_width=True)
        
        if submitted and journal_entry:
            journal_item = {
                "date": entry_date.isoformat(),
                "prompt": prompt,
                "entry": journal_entry,
                "feelings": feelings,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.compassion_journal.append(journal_item)
            if save_compassion_journal(st.session_state.compassion_journal):
                st.success("✅ Journal entry saved!")
                st.balloons()
    
    # Show recent entries
    if st.session_state.compassion_journal:
        st.markdown("---")
        st.markdown("### 📖 Recent Journal Entries")
        
        recent_entries = sorted(
            st.session_state.compassion_journal,
            key=lambda x: x.get('date', ''),
            reverse=True
        )[:10]
        
        for entry in recent_entries:
            date_str = datetime.fromisoformat(entry['date']).strftime("%B %d, %Y")
            with st.expander(f"📝 {date_str} - {entry.get('prompt', 'No prompt')[:50]}..."):
                st.markdown(f"**Prompt:** {entry.get('prompt')}")
                if entry.get('feelings'):
                    st.markdown(f"**Feelings:** {', '.join(entry['feelings'])}")
                st.markdown("---")
                st.markdown(entry.get('entry', 'No entry'))


def render_education():
    """Render educational content about self-compassion."""
    st.markdown("### 📚 Understanding Self-Compassion")
    
    st.info("""
    **Self-compassion** is treating yourself with the same kindness, care, and understanding 
    you would offer to a good friend who is struggling. It's been shown to reduce anxiety and 
    depression while increasing resilience and well-being.
    """)
    
    st.markdown("---")
    st.markdown("### 🧩 The Three Components of Self-Compassion")
    st.caption("Based on Dr. Kristin Neff's research")
    
    for component, data in SELF_COMPASSION_COMPONENTS.items():
        with st.expander(f"{data['icon']} {component}", expanded=False):
            st.markdown(f"**Definition:**")
            st.info(data['description'])
            
            st.markdown(f"**Practices:**")
            for practice in data['practices']:
                st.markdown(f"• {practice}")
    
    st.markdown("---")
    st.markdown("### 🔬 The Science of Self-Compassion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Benefits of Self-Compassion:**")
        st.success("""
        • Reduced anxiety and depression
        • Increased emotional resilience
        • Greater life satisfaction
        • Better stress management
        • Improved relationships
        • Enhanced motivation
        • Reduced rumination
        • Better coping with failure
        """)
    
    with col2:
        st.markdown("**Common Myths:**")
        st.warning("""
        **Myth:** Self-compassion is self-pity
        **Reality:** It's acknowledging struggle without exaggeration
        
        **Myth:** It makes you weak or lazy
        **Reality:** It increases motivation and resilience
        
        **Myth:** It's selfish
        **Reality:** It helps you care for others better
        
        **Myth:** Self-criticism motivates change
        **Reality:** Self-compassion is more effective
        """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips for Cultivating Self-Compassion")
    
    st.markdown("""
    **Daily Practices:**
    1. **Notice self-criticism** - Become aware of your inner critic
    2. **Pause and acknowledge** - "This is a moment of suffering"
    3. **Remember common humanity** - "Others feel this way too"
    4. **Offer kindness** - Speak to yourself as you would a friend
    5. **Practice regularly** - Use the exercises in this tool daily
    
    **When You're Struggling:**
    - Place hand over heart (physical gesture of kindness)
    - Take three deep breaths
    - Use the Self-Compassion Break
    - Write in your compassion journal
    - Read a compassionate letter you wrote yourself
    
    **Building the Habit:**
    - Start with small moments
    - Practice when things are going well
    - Be patient with yourself (yes, even here!)
    - Track your progress
    - Celebrate small wins
    """)
    
    st.markdown("---")
    st.markdown("### 📱 Additional Resources")
    
    st.markdown("""
    **Books:**
    - "Self-Compassion" by Dr. Kristin Neff
    - "The Mindful Self-Compassion Workbook" by Neff & Germer
    - "Radical Compassion" by Tara Brach
    
    **Websites:**
    - [self-compassion.org](https://self-compassion.org) - Dr. Kristin Neff's website
    - Free guided meditations and exercises
    - Self-compassion tests and resources
    
    **Research:**
    - Over 1000 scientific studies support self-compassion
    - Shown to be more sustainable than self-esteem
    - Effective across cultures and populations
    """)


def render_progress_tracker():
    """Render practice progress tracker."""
    st.markdown("### 📊 Your Self-Compassion Practice")
    
    if not st.session_state.compassion_practices:
        st.info("Start practicing to track your progress! Your practices will appear here.")
        return
    
    # Statistics
    total_practices = len(st.session_state.compassion_practices)
    breaks = sum(1 for p in st.session_state.compassion_practices if p.get('type') == 'Self-Compassion Break')
    comparisons = sum(1 for p in st.session_state.compassion_practices if p.get('type') == 'Criticism Comparison')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Practices", total_practices)
    with col2:
        st.metric("Compassion Breaks", breaks)
    with col3:
        st.metric("Comparisons", comparisons)
    with col4:
        st.metric("Journal Entries", len(st.session_state.compassion_journal))
    
    # Recent activity
    st.markdown("---")
    st.markdown("### 🕐 Recent Practice Activity")
    
    recent_practices = sorted(
        st.session_state.compassion_practices,
        key=lambda x: x.get('timestamp', ''),
        reverse=True
    )[:10]
    
    for practice in recent_practices:
        date_str = datetime.fromisoformat(practice['timestamp']).strftime("%B %d, %Y at %I:%M %p")
        practice_type = practice.get('type', 'Unknown')
        
        with st.expander(f"✨ {practice_type} - {date_str}"):
            if practice_type == "Self-Compassion Break":
                st.markdown(f"**🧘‍♀️ Mindfulness:** {practice.get('mindfulness')}")
                st.markdown(f"**🌍 Common Humanity:** {practice.get('common_humanity')}")
                st.markdown(f"**💝 Self-Kindness:** {practice.get('self_kindness')}")
            elif practice_type == "Criticism Comparison":
                st.markdown(f"**Situation:** {practice.get('situation')}")
                st.markdown(f"**❌ Self-Critical:** {practice.get('self_critical')}")
                st.markdown(f"**✅ Self-Compassionate:** {practice.get('self_compassionate')}")


def render_self_compassion_tool():
    """Main render function for self-compassion practice tool."""
    st.header("🌱 Self-Compassion Practice Tool")
    
    # Initialize state
    initialize_compassion_state()
    
    # Introduction
    st.info("""
    💝 Welcome to the Self-Compassion Practice Tool. Here you'll find guided exercises based on 
    Dr. Kristin Neff's research to help you develop self-kindness, recognize common humanity, 
    and practice mindfulness. Self-compassion is strongly linked to reduced anxiety and depression 
    and increased resilience.
    """)
    
    # Tab navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🫂 Compassion Break",
        "💌 Write Letter",
        "⚖️ Criticism vs Compassion",
        "📓 Journal",
        "📊 Progress",
        "📚 Learn"
    ])
    
    with tab1:
        st.markdown("""
        A quick practice you can use anytime you're struggling. It takes just a few minutes 
        and helps you respond to difficulty with kindness.
        """)
        render_compassion_break()
    
    with tab2:
        st.markdown("""
        Write a compassionate letter to yourself as if you were writing to a dear friend. 
        This powerful exercise can shift how you relate to yourself.
        """)
        render_compassionate_letter()
    
    with tab3:
        st.markdown("""
        Compare self-critical and self-compassionate responses to difficult situations. 
        Learn to recognize and replace harsh self-talk with kindness.
        """)
        render_criticism_comparison()
    
    with tab4:
        st.markdown("""
        Daily self-compassion journaling with prompts. Reflect on your experiences with 
        kindness and track your emotional patterns.
        """)
        render_compassion_journal()
    
    with tab5:
        st.markdown("""
        Track your self-compassion practice over time. See how consistent practice 
        builds the habit of treating yourself with kindness.
        """)
        render_progress_tracker()
    
    with tab6:
        render_education()
