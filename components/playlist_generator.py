import streamlit as st
import os
import json
from datetime import datetime
import pygame
import random

# Initialize pygame mixer for audio playback
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except:
    st.warning("Audio playback may not work properly. Please ensure pygame is installed.")

# Audio files directory
AUDIO_FILES_DIR = "audio_files"

# Define mood-based playlist categories
MOOD_PLAYLISTS = {
    "energizing": {
        "icon": "⚡",
        "name": "Energizing",
        "description": "Boost your mood and energy when feeling low",
        "purpose": "For combating low mood, fatigue, or lack of motivation",
        "benefits": ["Increases energy", "Boosts motivation", "Lifts spirits", "Enhances alertness"],
        "audio_files": ["gentle_piano.wav", "tibetan_bowls.wav"],
        "color": "#FF6B6B"
    },
    "calming": {
        "icon": "🌊",
        "name": "Calming",
        "description": "Reduce anxiety and find inner peace",
        "purpose": "For managing anxiety, stress, or overwhelming feelings",
        "benefits": ["Reduces anxiety", "Promotes relaxation", "Slows heart rate", "Eases tension"],
        "audio_files": ["ocean_waves.wav", "rain_sounds.wav", "forest_ambience.wav"],
        "color": "#4ECDC4"
    },
    "focus": {
        "icon": "🎯",
        "name": "Focus & Concentration",
        "description": "Enhance productivity and mental clarity",
        "purpose": "For work, study, or tasks requiring concentration",
        "benefits": ["Improves focus", "Enhances productivity", "Reduces distractions", "Supports deep work"],
        "audio_files": ["silent_soft_music.wav", "gentle_piano.wav"],
        "color": "#95E1D3"
    },
    "sleep": {
        "icon": "🌙",
        "name": "Sleep & Rest",
        "description": "Prepare for restful sleep",
        "purpose": "For bedtime routine and combating insomnia",
        "benefits": ["Promotes sleep", "Reduces racing thoughts", "Calms nervous system", "Creates bedtime ritual"],
        "audio_files": ["rain_sounds.wav", "ocean_waves.wav", "forest_ambience.wav"],
        "color": "#5E63B6"
    },
    "meditation": {
        "icon": "🧘",
        "name": "Meditation & Mindfulness",
        "description": "Deepen your meditation practice",
        "purpose": "For mindfulness practice and spiritual connection",
        "benefits": ["Deepens meditation", "Enhances mindfulness", "Spiritual grounding", "Present moment awareness"],
        "audio_files": ["tibetan_bowls.wav", "forest_ambience.wav", "silent_soft_music.wav"],
        "color": "#A8E6CF"
    },
    "grounding": {
        "icon": "🌳",
        "name": "Grounding & Stability",
        "description": "Feel connected and centered",
        "purpose": "For dissociation, panic, or feeling unmoored",
        "benefits": ["Grounds to present", "Reduces dissociation", "Creates safety", "Stabilizes emotions"],
        "audio_files": ["forest_ambience.wav", "rain_sounds.wav"],
        "color": "#8B7355"
    }
}

# Session state initialization
def initialize_playlist_state():
    """Initialize session state variables for playlist generator"""
    if "playlist_history" not in st.session_state:
        st.session_state.playlist_history = []
    if "playlist_favorites" not in st.session_state:
        st.session_state.playlist_favorites = []
    if "current_playlist" not in st.session_state:
        st.session_state.current_playlist = None
    if "current_track_index" not in st.session_state:
        st.session_state.current_track_index = 0
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False
    if "track_ratings" not in st.session_state:
        st.session_state.track_ratings = {}
    if "playlist_effectiveness" not in st.session_state:
        st.session_state.playlist_effectiveness = {}

def save_playlist_history(mood_type, rating=None, notes=""):
    """Save playlist usage to history"""
    entry = {
        "mood_type": mood_type,
        "timestamp": datetime.now().isoformat(),
        "rating": rating,
        "notes": notes
    }
    st.session_state.playlist_history.append(entry)
    # Keep only last 50 entries
    if len(st.session_state.playlist_history) > 50:
        st.session_state.playlist_history = st.session_state.playlist_history[-50:]

def play_audio(audio_file):
    """Play audio file using pygame"""
    try:
        audio_path = os.path.join(AUDIO_FILES_DIR, audio_file)
        if os.path.exists(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            st.session_state.is_playing = True
            return True
        else:
            st.warning(f"Audio file not found: {audio_file}")
            return False
    except Exception as e:
        st.error(f"Error playing audio: {str(e)}")
        return False

def stop_audio():
    """Stop audio playback"""
    try:
        pygame.mixer.music.stop()
        st.session_state.is_playing = False
    except:
        pass

def render_playlist_card(mood_key, playlist_data):
    """Render a playlist card"""
    with st.container():
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {playlist_data['color']}20 0%, {playlist_data['color']}40 100%);
            border-left: 5px solid {playlist_data['color']};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        ">
            <h3 style="color: {playlist_data['color']}; margin: 0;">
                {playlist_data['icon']} {playlist_data['name']}
            </h3>
            <p style="color: #555; margin: 0.5rem 0;">{playlist_data['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Details"):
            st.markdown(f"**Purpose:** {playlist_data['purpose']}")
            st.markdown("**Benefits:**")
            for benefit in playlist_data['benefits']:
                st.markdown(f"- {benefit}")
            st.markdown(f"**Tracks:** {len(playlist_data['audio_files'])} audio files")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button(f"▶️ Play {playlist_data['name']}", key=f"play_{mood_key}", use_container_width=True):
                st.session_state.current_playlist = mood_key
                st.session_state.current_track_index = 0
                save_playlist_history(mood_key)
                st.rerun()
        
        with col2:
            is_favorited = mood_key in st.session_state.playlist_favorites
            if st.button("⭐" if is_favorited else "☆", key=f"fav_{mood_key}", use_container_width=True):
                if is_favorited:
                    st.session_state.playlist_favorites.remove(mood_key)
                else:
                    st.session_state.playlist_favorites.append(mood_key)
                st.rerun()
        
        with col3:
            if st.button("📊", key=f"stats_{mood_key}", use_container_width=True):
                st.session_state[f"show_stats_{mood_key}"] = not st.session_state.get(f"show_stats_{mood_key}", False)
                st.rerun()
        
        # Show stats if toggled
        if st.session_state.get(f"show_stats_{mood_key}", False):
            usage_count = sum(1 for entry in st.session_state.playlist_history if entry["mood_type"] == mood_key)
            avg_rating = 0
            rated_entries = [entry for entry in st.session_state.playlist_history 
                           if entry["mood_type"] == mood_key and entry.get("rating")]
            if rated_entries:
                avg_rating = sum(entry["rating"] for entry in rated_entries) / len(rated_entries)
            
            st.info(f"Used {usage_count} times | Average rating: {avg_rating:.1f}/5 ⭐")

def render_player():
    """Render the audio player for current playlist"""
    if st.session_state.current_playlist:
        playlist = MOOD_PLAYLISTS[st.session_state.current_playlist]
        
        st.markdown("---")
        st.markdown("### 🎵 Now Playing")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {playlist['color']}30 0%, {playlist['color']}50 100%);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        ">
            <h2 style="color: {playlist['color']}; text-align: center; margin: 0;">
                {playlist['icon']} {playlist['name']}
            </h2>
            <p style="text-align: center; color: #666; margin-top: 0.5rem;">
                {playlist['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Track information
        if st.session_state.current_track_index < len(playlist['audio_files']):
            current_track = playlist['audio_files'][st.session_state.current_track_index]
            track_name = current_track.replace('.wav', '').replace('_', ' ').title()
            
            st.markdown(f"**Track {st.session_state.current_track_index + 1} of {len(playlist['audio_files'])}:** {track_name}")
            
            # Player controls
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button("⏮️ Previous", use_container_width=True):
                    stop_audio()
                    if st.session_state.current_track_index > 0:
                        st.session_state.current_track_index -= 1
                    st.rerun()
            
            with col2:
                if st.session_state.is_playing:
                    if st.button("⏸️ Pause", use_container_width=True):
                        stop_audio()
                        st.rerun()
                else:
                    if st.button("▶️ Play", use_container_width=True):
                        play_audio(current_track)
                        st.rerun()
            
            with col3:
                if st.button("⏹️ Stop", use_container_width=True):
                    stop_audio()
                    st.session_state.current_playlist = None
                    st.session_state.current_track_index = 0
                    st.rerun()
            
            with col4:
                if st.button("⏭️ Next", use_container_width=True):
                    stop_audio()
                    if st.session_state.current_track_index < len(playlist['audio_files']) - 1:
                        st.session_state.current_track_index += 1
                    st.rerun()
            
            with col5:
                if st.button("🔀 Shuffle", use_container_width=True):
                    stop_audio()
                    st.session_state.current_track_index = random.randint(0, len(playlist['audio_files']) - 1)
                    st.rerun()
            
            # Volume control
            st.markdown("**Volume Control**")
            volume = st.slider("", 0, 100, 70, key="volume_slider", label_visibility="collapsed")
            pygame.mixer.music.set_volume(volume / 100.0)
            
            # Rating section
            st.markdown("---")
            st.markdown("### How effective was this playlist?")
            rating = st.slider("Rate this session (1-5 stars)", 1, 5, 3, key=f"rating_{st.session_state.current_playlist}")
            notes = st.text_area("Optional notes about your experience:", key=f"notes_{st.session_state.current_playlist}", height=80)
            
            if st.button("💾 Save Rating", use_container_width=True):
                save_playlist_history(st.session_state.current_playlist, rating, notes)
                st.success("Rating saved! Thank you for your feedback.")
                st.balloons()

def render_mood_assessment():
    """Quick mood assessment to suggest playlists"""
    st.markdown("### 🎯 Quick Mood Check")
    st.markdown("Tell us how you're feeling, and we'll suggest the perfect playlist:")
    
    mood_options = {
        "😔 Low energy/motivation": "energizing",
        "😰 Anxious/stressed": "calming",
        "😴 Need focus": "focus",
        "😖 Can't sleep": "sleep",
        "🤔 Want to meditate": "meditation",
        "😵 Feeling ungrounded": "grounding"
    }
    
    selected_mood = st.radio("Select your current state:", options=list(mood_options.keys()), key="mood_assessment")
    
    if st.button("Get Recommendation", use_container_width=True):
        recommended_playlist = mood_options[selected_mood]
        st.success(f"We recommend: {MOOD_PLAYLISTS[recommended_playlist]['icon']} {MOOD_PLAYLISTS[recommended_playlist]['name']}")
        st.markdown(f"**Why:** {MOOD_PLAYLISTS[recommended_playlist]['purpose']}")
        
        if st.button(f"▶️ Start {MOOD_PLAYLISTS[recommended_playlist]['name']}", use_container_width=True):
            st.session_state.current_playlist = recommended_playlist
            st.session_state.current_track_index = 0
            save_playlist_history(recommended_playlist)
            st.rerun()

def render_statistics():
    """Show playlist usage statistics"""
    if st.session_state.playlist_history:
        st.markdown("### 📊 Your Listening History")
        
        # Count usage per playlist
        usage_counts = {}
        for entry in st.session_state.playlist_history:
            mood = entry["mood_type"]
            usage_counts[mood] = usage_counts.get(mood, 0) + 1
        
        # Display as bars
        for mood, count in sorted(usage_counts.items(), key=lambda x: x[1], reverse=True):
            playlist = MOOD_PLAYLISTS[mood]
            percentage = (count / len(st.session_state.playlist_history)) * 100
            st.markdown(f"""
            <div style="margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
                    <span>{playlist['icon']} {playlist['name']}</span>
                    <span>{count} times ({percentage:.0f}%)</span>
                </div>
                <div style="
                    width: 100%;
                    height: 20px;
                    background: #f0f0f0;
                    border-radius: 10px;
                    overflow: hidden;
                ">
                    <div style="
                        width: {percentage}%;
                        height: 100%;
                        background: {playlist['color']};
                    "></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent sessions
        st.markdown("### 🕐 Recent Sessions")
        recent_sessions = st.session_state.playlist_history[-5:][::-1]
        for entry in recent_sessions:
            playlist = MOOD_PLAYLISTS[entry["mood_type"]]
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%b %d, %Y at %I:%M %p")
            rating_display = "⭐" * entry.get("rating", 0) if entry.get("rating") else "Not rated"
            st.markdown(f"**{playlist['icon']} {playlist['name']}** - {timestamp} - {rating_display}")
            if entry.get("notes"):
                st.markdown(f"*{entry['notes']}*")

def render_playlist_generator():
    """Main function to render the Personalized Playlist Generator"""
    initialize_playlist_state()
    
    st.header("🎵 Personalized Playlist Generator for Mood Regulation")
    
    st.markdown("""
    Music therapy is a powerful tool for emotional regulation. Our curated playlists are designed to help you:
    - **Energize** when feeling low
    - **Calm** anxiety and stress
    - **Focus** for productivity
    - **Sleep** better
    - **Meditate** deeper
    - **Ground** yourself in difficult moments
    
    Each playlist is carefully crafted with therapeutic audio to support your mental well-being.
    """)
    
    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs(["🎵 Browse Playlists", "🎯 Quick Mood Check", "📊 Statistics", "⭐ Favorites"])
    
    with tab1:
        st.markdown("### Browse All Mood Playlists")
        
        # Search/filter
        search_query = st.text_input("Search playlists...", placeholder="e.g., anxiety, sleep, focus")
        
        for mood_key, playlist_data in MOOD_PLAYLISTS.items():
            # Filter by search query
            if search_query:
                if search_query.lower() not in playlist_data['name'].lower() and \
                   search_query.lower() not in playlist_data['description'].lower() and \
                   search_query.lower() not in playlist_data['purpose'].lower():
                    continue
            
            render_playlist_card(mood_key, playlist_data)
    
    with tab2:
        render_mood_assessment()
    
    with tab3:
        render_statistics()
    
    with tab4:
        st.markdown("### ⭐ Your Favorite Playlists")
        if st.session_state.playlist_favorites:
            for mood_key in st.session_state.playlist_favorites:
                render_playlist_card(mood_key, MOOD_PLAYLISTS[mood_key])
        else:
            st.info("You haven't added any favorites yet. Click the ☆ button on any playlist to add it to your favorites.")
    
    # Render player if a playlist is active
    if st.session_state.current_playlist:
        render_player()
    
    # Help section
    with st.expander("ℹ️ How to Use This Tool"):
        st.markdown("""
        **Getting Started:**
        1. Browse available playlists or use the Quick Mood Check
        2. Click "Play" on a playlist that matches your needs
        3. Adjust volume and navigate between tracks
        4. Rate your experience to help personalize future recommendations
        
        **Tips for Best Results:**
        - Use headphones for an immersive experience
        - Find a quiet, comfortable space
        - Allow 10-15 minutes minimum for full effect
        - Combine with deep breathing or meditation
        - Rate playlists to track what works best for you
        
        **Music Therapy Benefits:**
        - Reduces cortisol (stress hormone)
        - Releases dopamine (feel-good chemical)
        - Regulates heart rate and blood pressure
        - Improves sleep quality
        - Enhances focus and concentration
        - Supports emotional processing
        """)

# Main render function
if __name__ == "__main__":
    render_playlist_generator()
