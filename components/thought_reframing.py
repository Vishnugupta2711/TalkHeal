"""
Thought Reframing Assistant - CBT Tool Component
Helps users identify negative thought patterns and reframe them into more balanced perspectives.
"""

import streamlit as st
from datetime import datetime
import json
import os

# Cognitive distortions with descriptions and examples
COGNITIVE_DISTORTIONS = {
    "All-or-Nothing Thinking": {
        "description": "Seeing things in black and white categories. If something isn't perfect, it's a total failure.",
        "examples": [
            "I made one mistake, so I'm a complete failure.",
            "If I don't do this perfectly, there's no point in trying."
        ],
        "icon": "⚫⚪"
    },
    "Overgeneralization": {
        "description": "Seeing a single negative event as a never-ending pattern of defeat.",
        "examples": [
            "I failed this test, so I'll never succeed at anything.",
            "They didn't call me back, nobody ever likes me."
        ],
        "icon": "🔁"
    },
    "Mental Filter": {
        "description": "Focusing only on negative details while filtering out all the positive aspects of a situation.",
        "examples": [
            "The presentation went well except for one question I couldn't answer - it was a disaster.",
            "I got 9 compliments and 1 criticism - I must be doing terrible."
        ],
        "icon": "🔍"
    },
    "Discounting the Positive": {
        "description": "Rejecting positive experiences by insisting they 'don't count' for some reason.",
        "examples": [
            "Sure, I got the promotion, but only because they felt sorry for me.",
            "They said I did well, but they're just being nice."
        ],
        "icon": "❌"
    },
    "Jumping to Conclusions": {
        "description": "Making negative interpretations without actual evidence (mind reading or fortune telling).",
        "examples": [
            "They're definitely angry with me (without asking).",
            "I know this interview will go badly before it even starts."
        ],
        "icon": "🔮"
    },
    "Magnification/Catastrophizing": {
        "description": "Exaggerating the importance of problems or shortcomings, or minimizing your positive qualities.",
        "examples": [
            "I made a small error, and now everything is ruined!",
            "If I make a mistake in this meeting, I'll lose my job and my career will be over."
        ],
        "icon": "🔥"
    },
    "Emotional Reasoning": {
        "description": "Assuming that negative emotions necessarily reflect the way things really are.",
        "examples": [
            "I feel anxious, so something bad must be about to happen.",
            "I feel like a loser, therefore I am a loser."
        ],
        "icon": "💭"
    },
    "Should Statements": {
        "description": "Trying to motivate yourself with 'shoulds' and 'musts', leading to guilt and frustration.",
        "examples": [
            "I should be able to handle this without getting stressed.",
            "I must always be productive, or I'm wasting my life."
        ],
        "icon": "⚠️"
    },
    "Labeling": {
        "description": "Attaching a negative label to yourself or others instead of describing the specific behavior.",
        "examples": [
            "I'm a loser. (instead of 'I didn't do well on this task')",
            "They're a jerk. (instead of 'They acted rudely in that situation')"
        ],
        "icon": "🏷️"
    },
    "Personalization": {
        "description": "Seeing yourself as the cause of negative external events when you weren't primarily responsible.",
        "examples": [
            "The meeting went badly, it must be my fault.",
            "My friend is in a bad mood, I must have done something wrong."
        ],
        "icon": "👉"
    }
}

# Reframing questions to guide users
REFRAMING_QUESTIONS = [
    "What evidence do I have that this thought is true?",
    "What evidence contradicts this thought?",
    "Am I confusing a thought with a fact?",
    "What would I tell a friend who had this thought?",
    "Am I looking at the whole picture or just focusing on one part?",
    "What are alternative ways to look at this situation?",
    "What's the worst that could realistically happen?",
    "What's the best that could happen?",
    "What's most likely to happen?",
    "If the worst happens, how could I cope?",
    "Will this matter in a year? In five years?",
    "Am I being too hard on myself?",
    "What would be a more balanced way to think about this?"
]


def initialize_reframing_state():
    """Initialize session state for thought reframing tool."""
    if "reframing_step" not in st.session_state:
        st.session_state.reframing_step = 0
    if "reframing_data" not in st.session_state:
        st.session_state.reframing_data = {
            "negative_thought": "",
            "situation": "",
            "emotions": [],
            "intensity": 5,
            "distortions": [],
            "evidence_for": "",
            "evidence_against": "",
            "alternative_thoughts": [],
            "reframed_thought": "",
            "new_intensity": 5,
            "timestamp": None
        }
    if "saved_reframings" not in st.session_state:
        st.session_state.saved_reframings = load_saved_reframings()


def load_saved_reframings():
    """Load saved thought reframings from file."""
    try:
        if os.path.exists("data/thought_reframings.json"):
            with open("data/thought_reframings.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load saved reframings: {e}")
    return []


def save_reframing_to_file(reframing_data):
    """Save a thought reframing to file."""
    try:
        os.makedirs("data", exist_ok=True)
        saved_reframings = load_saved_reframings()
        saved_reframings.append(reframing_data)
        with open("data/thought_reframings.json", "w") as f:
            json.dump(saved_reframings, f, indent=2)
        st.session_state.saved_reframings = saved_reframings
        return True
    except Exception as e:
        st.error(f"Could not save reframing: {e}")
        return False


def render_step_indicator(current_step, total_steps):
    """Render a visual step indicator."""
    cols = st.columns(total_steps)
    for i in range(total_steps):
        with cols[i]:
            if i < current_step:
                st.markdown(f"✅ Step {i+1}")
            elif i == current_step:
                st.markdown(f"**▶️ Step {i+1}**")
            else:
                st.markdown(f"⚪ Step {i+1}")


def render_step_1():
    """Step 1: Identify the negative thought and situation."""
    st.subheader("Step 1: Identify Your Thought")
    st.info("👋 Let's start by capturing the negative thought that's bothering you.")
    
    st.markdown("**What's the situation?**")
    st.caption("Briefly describe what happened or what's happening.")
    situation = st.text_area(
        "Situation:",
        value=st.session_state.reframing_data["situation"],
        placeholder="Example: I got critical feedback at work today...",
        height=80,
        key="situation_input"
    )
    
    st.markdown("**What's the automatic negative thought?**")
    st.caption("What went through your mind? Write it exactly as you thought it.")
    negative_thought = st.text_area(
        "Negative Thought:",
        value=st.session_state.reframing_data["negative_thought"],
        placeholder="Example: I'm terrible at my job and everyone thinks I'm incompetent...",
        height=100,
        key="negative_thought_input"
    )
    
    st.markdown("**What emotions are you feeling?**")
    st.caption("Select all that apply.")
    emotion_options = [
        "Anxious", "Sad", "Angry", "Frustrated", "Ashamed", 
        "Guilty", "Hopeless", "Overwhelmed", "Fearful", "Disappointed"
    ]
    emotions = st.multiselect(
        "Emotions:",
        options=emotion_options,
        default=st.session_state.reframing_data["emotions"],
        key="emotions_input"
    )
    
    st.markdown("**How intense is this feeling? (1 = mild, 10 = extreme)**")
    intensity = st.slider(
        "Intensity:",
        min_value=1,
        max_value=10,
        value=st.session_state.reframing_data["intensity"],
        key="intensity_input"
    )
    
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Next Step →", use_container_width=True, type="primary"):
            if not negative_thought.strip():
                st.warning("Please enter your negative thought before continuing.")
            else:
                st.session_state.reframing_data["situation"] = situation
                st.session_state.reframing_data["negative_thought"] = negative_thought
                st.session_state.reframing_data["emotions"] = emotions
                st.session_state.reframing_data["intensity"] = intensity
                st.session_state.reframing_step = 1
                st.rerun()


def render_step_2():
    """Step 2: Identify cognitive distortions."""
    st.subheader("Step 2: Identify Thinking Patterns")
    st.info("🔍 Let's identify if any common thinking traps are present in your thought.")
    
    # Show the original thought for reference
    with st.expander("📝 Your Original Thought", expanded=False):
        st.write(f"**Thought:** {st.session_state.reframing_data['negative_thought']}")
        st.write(f"**Emotions:** {', '.join(st.session_state.reframing_data['emotions'])}")
        st.write(f"**Intensity:** {st.session_state.reframing_data['intensity']}/10")
    
    st.markdown("**Common Cognitive Distortions**")
    st.caption("Select any thinking patterns you recognize in your thought. Click on each to see examples.")
    
    selected_distortions = []
    
    # Display distortions with expandable details
    for distortion_name, distortion_info in COGNITIVE_DISTORTIONS.items():
        with st.expander(f"{distortion_info['icon']} {distortion_name}"):
            st.markdown(f"**Description:** {distortion_info['description']}")
            st.markdown("**Examples:**")
            for example in distortion_info['examples']:
                st.markdown(f"- *{example}*")
        
        if st.checkbox(
            f"My thought shows {distortion_name}",
            key=f"distortion_{distortion_name}",
            value=distortion_name in st.session_state.reframing_data["distortions"]
        ):
            selected_distortions.append(distortion_name)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous Step", use_container_width=True):
            st.session_state.reframing_step = 0
            st.rerun()
    
    with col2:
        if st.button("Next Step →", use_container_width=True, type="primary"):
            st.session_state.reframing_data["distortions"] = selected_distortions
            st.session_state.reframing_step = 2
            st.rerun()


def render_step_3():
    """Step 3: Examine the evidence."""
    st.subheader("Step 3: Examine the Evidence")
    st.info("⚖️ Let's look at the facts objectively, like a detective or scientist.")
    
    # Show the original thought for reference
    with st.expander("📝 Your Original Thought", expanded=False):
        st.write(f"**Thought:** {st.session_state.reframing_data['negative_thought']}")
        if st.session_state.reframing_data['distortions']:
            st.write(f"**Thinking patterns:** {', '.join(st.session_state.reframing_data['distortions'])}")
    
    st.markdown("**What evidence SUPPORTS this thought?**")
    st.caption("What facts or observations make this thought seem true? Be specific and objective.")
    evidence_for = st.text_area(
        "Evidence For:",
        value=st.session_state.reframing_data["evidence_for"],
        placeholder="List concrete facts that support this thought...",
        height=100,
        key="evidence_for_input"
    )
    
    st.markdown("**What evidence CONTRADICTS this thought?**")
    st.caption("What facts or observations suggest this thought might not be completely true?")
    evidence_against = st.text_area(
        "Evidence Against:",
        value=st.session_state.reframing_data["evidence_against"],
        placeholder="List facts that contradict or weaken this thought...",
        height=100,
        key="evidence_against_input"
    )
    
    st.markdown("**Reflection Questions:**")
    with st.expander("Click to see helpful questions"):
        for question in REFRAMING_QUESTIONS[:7]:
            st.markdown(f"- {question}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous Step", use_container_width=True):
            st.session_state.reframing_data["evidence_for"] = evidence_for
            st.session_state.reframing_data["evidence_against"] = evidence_against
            st.session_state.reframing_step = 1
            st.rerun()
    
    with col2:
        if st.button("Next Step →", use_container_width=True, type="primary"):
            st.session_state.reframing_data["evidence_for"] = evidence_for
            st.session_state.reframing_data["evidence_against"] = evidence_against
            st.session_state.reframing_step = 3
            st.rerun()


def render_step_4():
    """Step 4: Generate alternative thoughts."""
    st.subheader("Step 4: Create Alternative Thoughts")
    st.info("💡 Let's develop more balanced, realistic ways of thinking about this situation.")
    
    # Show the original thought for reference
    with st.expander("📝 Review Your Analysis", expanded=False):
        st.write(f"**Original Thought:** {st.session_state.reframing_data['negative_thought']}")
        if st.session_state.reframing_data['evidence_for']:
            st.write(f"**Evidence For:** {st.session_state.reframing_data['evidence_for']}")
        if st.session_state.reframing_data['evidence_against']:
            st.write(f"**Evidence Against:** {st.session_state.reframing_data['evidence_against']}")
    
    st.markdown("**Alternative Perspectives**")
    st.caption("Brainstorm different ways to think about this situation. Be compassionate and realistic.")
    
    # Allow multiple alternative thoughts
    num_alternatives = st.number_input(
        "How many alternatives would you like to create?",
        min_value=1,
        max_value=5,
        value=max(1, len(st.session_state.reframing_data.get("alternative_thoughts", []))),
        key="num_alternatives"
    )
    
    alternative_thoughts = []
    for i in range(int(num_alternatives)):
        default_value = ""
        if i < len(st.session_state.reframing_data.get("alternative_thoughts", [])):
            default_value = st.session_state.reframing_data["alternative_thoughts"][i]
        
        alt_thought = st.text_area(
            f"Alternative Thought #{i+1}:",
            value=default_value,
            placeholder=f"Example: While I made a mistake, I've also done many things well. One error doesn't define my entire performance...",
            height=80,
            key=f"alt_thought_{i}"
        )
        if alt_thought.strip():
            alternative_thoughts.append(alt_thought)
    
    st.markdown("**More Reframing Questions:**")
    with st.expander("Click to see more helpful questions"):
        for question in REFRAMING_QUESTIONS[7:]:
            st.markdown(f"- {question}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous Step", use_container_width=True):
            st.session_state.reframing_data["alternative_thoughts"] = alternative_thoughts
            st.session_state.reframing_step = 2
            st.rerun()
    
    with col2:
        if st.button("Next Step →", use_container_width=True, type="primary"):
            if not alternative_thoughts:
                st.warning("Please create at least one alternative thought before continuing.")
            else:
                st.session_state.reframing_data["alternative_thoughts"] = alternative_thoughts
                st.session_state.reframing_step = 4
                st.rerun()


def render_step_5():
    """Step 5: Create the final reframed thought."""
    st.subheader("Step 5: Your Reframed Thought")
    st.info("✨ Now, let's create your balanced, reframed thought based on your analysis.")
    
    # Show alternatives for reference
    with st.expander("📝 Review Your Alternative Thoughts", expanded=True):
        for i, alt in enumerate(st.session_state.reframing_data["alternative_thoughts"], 1):
            st.markdown(f"**{i}.** {alt}")
    
    st.markdown("**Your Final Reframed Thought**")
    st.caption("Combine the best elements of your alternatives into one balanced, realistic thought.")
    reframed_thought = st.text_area(
        "Reframed Thought:",
        value=st.session_state.reframing_data["reframed_thought"],
        placeholder="Write a balanced thought that acknowledges reality while being fair and compassionate to yourself...",
        height=120,
        key="reframed_thought_input"
    )
    
    st.markdown("**How intense do you feel now? (1 = mild, 10 = extreme)**")
    st.caption("Rate your emotional intensity after reframing.")
    new_intensity = st.slider(
        "New Intensity:",
        min_value=1,
        max_value=10,
        value=st.session_state.reframing_data.get("new_intensity", st.session_state.reframing_data["intensity"]),
        key="new_intensity_input"
    )
    
    # Show intensity comparison
    old_intensity = st.session_state.reframing_data["intensity"]
    if new_intensity < old_intensity:
        st.success(f"📉 Your emotional intensity decreased from {old_intensity} to {new_intensity}!")
    elif new_intensity == old_intensity:
        st.info(f"Your emotional intensity remained at {new_intensity}. That's okay - sometimes awareness is the first step.")
    else:
        st.info(f"Your intensity is now {new_intensity}. This process takes practice - be patient with yourself.")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous Step", use_container_width=True):
            st.session_state.reframing_data["reframed_thought"] = reframed_thought
            st.session_state.reframing_data["new_intensity"] = new_intensity
            st.session_state.reframing_step = 3
            st.rerun()
    
    with col2:
        if st.button("Save & Finish", use_container_width=True, type="primary"):
            if not reframed_thought.strip():
                st.warning("Please create your reframed thought before finishing.")
            else:
                st.session_state.reframing_data["reframed_thought"] = reframed_thought
                st.session_state.reframing_data["new_intensity"] = new_intensity
                st.session_state.reframing_data["timestamp"] = datetime.now().isoformat()
                st.session_state.reframing_step = 5
                st.rerun()
    
    with col3:
        if st.button("Start Over", use_container_width=True):
            st.session_state.reframing_step = 0
            st.session_state.reframing_data = {
                "negative_thought": "",
                "situation": "",
                "emotions": [],
                "intensity": 5,
                "distortions": [],
                "evidence_for": "",
                "evidence_against": "",
                "alternative_thoughts": [],
                "reframed_thought": "",
                "new_intensity": 5,
                "timestamp": None
            }
            st.rerun()


def render_completion_summary():
    """Display the completion summary."""
    st.success("🎉 Congratulations! You've completed the thought reframing exercise!")
    
    data = st.session_state.reframing_data
    
    st.markdown("### Your Thought Reframing Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📉 Before")
        st.markdown(f"**Thought:** {data['negative_thought']}")
        if data['emotions']:
            st.markdown(f"**Emotions:** {', '.join(data['emotions'])}")
        st.markdown(f"**Intensity:** {data['intensity']}/10")
        if data['distortions']:
            st.markdown(f"**Thinking Patterns:** {', '.join(data['distortions'])}")
    
    with col2:
        st.markdown("#### 📈 After")
        st.markdown(f"**Reframed Thought:** {data['reframed_thought']}")
        st.markdown(f"**New Intensity:** {data['new_intensity']}/10")
        improvement = data['intensity'] - data['new_intensity']
        if improvement > 0:
            st.markdown(f"**Improvement:** ↓ {improvement} points")
    
    # Save option
    col_save, col_new = st.columns([1, 1])
    with col_save:
        if st.button("💾 Save This Reframing", use_container_width=True, type="primary"):
            if save_reframing_to_file(data):
                st.success("✅ Saved successfully!")
            else:
                st.error("Could not save. Please try again.")
    
    with col_new:
        if st.button("🔄 Start New Exercise", use_container_width=True):
            st.session_state.reframing_step = 0
            st.session_state.reframing_data = {
                "negative_thought": "",
                "situation": "",
                "emotions": [],
                "intensity": 5,
                "distortions": [],
                "evidence_for": "",
                "evidence_against": "",
                "alternative_thoughts": [],
                "reframed_thought": "",
                "new_intensity": 5,
                "timestamp": None
            }
            st.rerun()
    
    # Tips for continuing
    st.markdown("---")
    st.markdown("### 💡 Tips for Practice")
    st.info("""
    - **Practice regularly:** The more you practice, the more automatic balanced thinking becomes.
    - **Be patient:** Changing thought patterns takes time. Every small shift counts.
    - **Review your reframings:** Look back at past exercises to reinforce new patterns.
    - **Share with your therapist:** These records can be valuable in therapy sessions.
    - **Notice patterns:** Over time, you may identify your most common thinking traps.
    """)


def render_saved_reframings():
    """Display saved thought reframings."""
    if not st.session_state.saved_reframings:
        st.info("No saved reframings yet. Complete an exercise to save your first reframing!")
        return
    
    st.markdown(f"### 📚 Your Saved Reframings ({len(st.session_state.saved_reframings)})")
    
    # Sort by most recent first
    sorted_reframings = sorted(
        st.session_state.saved_reframings,
        key=lambda x: x.get('timestamp', ''),
        reverse=True
    )
    
    for i, reframing in enumerate(sorted_reframings):
        timestamp = reframing.get('timestamp', 'Unknown date')
        if timestamp != 'Unknown date':
            try:
                dt = datetime.fromisoformat(timestamp)
                timestamp = dt.strftime("%B %d, %Y at %I:%M %p")
            except:
                pass
        
        with st.expander(f"🗓️ {timestamp} - Intensity: {reframing.get('intensity', 'N/A')} → {reframing.get('new_intensity', 'N/A')}"):
            st.markdown(f"**Original Thought:** {reframing.get('negative_thought', 'N/A')}")
            st.markdown(f"**Reframed Thought:** {reframing.get('reframed_thought', 'N/A')}")
            
            if reframing.get('emotions'):
                st.markdown(f"**Emotions:** {', '.join(reframing['emotions'])}")
            
            if reframing.get('distortions'):
                st.markdown(f"**Thinking Patterns:** {', '.join(reframing['distortions'])}")
            
            improvement = reframing.get('intensity', 0) - reframing.get('new_intensity', 0)
            if improvement > 0:
                st.success(f"📉 Emotional intensity reduced by {improvement} points")


def render_thought_reframing():
    """Main render function for the thought reframing tool."""
    st.header("💭 Thought Reframing Assistant (CBT Tool)")
    
    # Initialize state
    initialize_reframing_state()
    
    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["✏️ New Exercise", "📚 Saved Reframings", "ℹ️ About CBT"])
    
    with tab1:
        st.markdown("""
        This tool uses **Cognitive Behavioral Therapy (CBT)** techniques to help you identify 
        and challenge negative thought patterns, replacing them with more balanced, realistic perspectives.
        """)
        
        # Step indicator
        total_steps = 5
        current_step = st.session_state.reframing_step
        
        if current_step < 5:
            render_step_indicator(current_step, total_steps)
            st.markdown("---")
        
        # Render appropriate step
        if current_step == 0:
            render_step_1()
        elif current_step == 1:
            render_step_2()
        elif current_step == 2:
            render_step_3()
        elif current_step == 3:
            render_step_4()
        elif current_step == 4:
            render_step_5()
        elif current_step == 5:
            render_completion_summary()
    
    with tab2:
        render_saved_reframings()
    
    with tab3:
        st.markdown("""
        ### What is Cognitive Behavioral Therapy (CBT)?
        
        **CBT** is one of the most researched and effective forms of psychotherapy. It's based on the idea 
        that our thoughts, feelings, and behaviors are interconnected. By changing negative thought patterns, 
        we can improve our emotions and behaviors.
        
        ### The CBT Triangle
        
        ```
           THOUGHTS
              ↗ ↘
        FEELINGS ←→ BEHAVIORS
        ```
        
        When we change our thoughts, we can influence both our feelings and actions.
        
        ### What are Cognitive Distortions?
        
        Cognitive distortions are irrational thought patterns that can negatively affect how we perceive 
        reality. Everyone experiences them, but they become problematic when they're frequent or intense.
        
        ### How This Tool Helps
        
        This tool guides you through a structured process to:
        1. **Identify** negative automatic thoughts
        2. **Recognize** cognitive distortions (thinking traps)
        3. **Examine** the evidence objectively
        4. **Generate** alternative, balanced perspectives
        5. **Create** a reframed thought that's more realistic and compassionate
        
        ### When to Use This Tool
        
        - When you notice persistent negative thoughts
        - Before or after stressful situations
        - When emotions feel overwhelming
        - As regular practice to build mental resilience
        - In conjunction with therapy (share your reframings with your therapist!)
        
        ### Important Notes
        
        - This tool is for **self-help and learning**, not a replacement for professional therapy
        - If you're experiencing severe distress, please reach out to a mental health professional
        - Practice makes progress - be patient with yourself as you learn these skills
        - Some thoughts are harder to reframe than others, and that's okay
        
        ### Resources
        
        - **Feeling Good: The New Mood Therapy** by David Burns, MD
        - **Mind Over Mood** by Dennis Greenberger and Christine Padesky
        - **The Anxiety and Worry Workbook** by David Clark and Aaron Beck
        """)
