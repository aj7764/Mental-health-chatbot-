import streamlit as st
import random
import time
import pygame
def main():
    
    pygame.mixer.init()
    correct_sound = "correct.wav"
    wrong_sound = "wrong.wav"

    def play_sound(result):
        try:
            if result:
                pygame.mixer.Sound(correct_sound).play()
            else:
                pygame.mixer.Sound(wrong_sound).play()
        except pygame.error:
                st.warning("Sound effects not available.")

# Game Constants
    BASE_GRID_SIZE = 4
    BASE_PATTERN_LENGTH = 5
    HINT_LIMIT = 3  # Max hints allowed per game

    def get_difficulty_settings(level):
        return BASE_GRID_SIZE + (level // 2), BASE_PATTERN_LENGTH + level

    def generate_pattern(grid_size, pattern_length):
        return [(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(pattern_length)]

# Background and Style
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #ffffff;
        }
        .stApp {
            background: linear-gradient(135deg, #ff7e5f, #feb47b);
            color: #ffffff;
        }
        .stButton>button {
            border-radius: 10px;
            padding: 12px 25px;
            font-size: 18px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #ff4757 !important;
            color: white !important;
            box-shadow: 0 0 10px #ff6b81;
        }
        .sidebar {
            background: #1e3a8a !important;
            color: white;
            padding: 20px;
        }
        .sidebar .stText {
            color: white;
        }
        .leaderboard-badge {
            padding: 10px 15px;
            border-radius: 15px;
            background: #ff6b81;
            color: white;
            display: inline-block;
            margin-bottom: 10px;
        }
        .score-badge {
            background: #00c851;
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Display the grid
    def display_grid(grid_size, pattern=[], reveal=False, selected_cells=[], hint=False):
        new_selected_cells = selected_cells.copy()

        for row in range(grid_size):
            cols = st.columns(grid_size)
            for col in range(grid_size):
                cell_key = f"{row}_{col}"

                if reveal and (row, col) in pattern:
                    cols[col].button("✅", key=cell_key, help="Pattern Cell", use_container_width=True)
                elif hint and (row, col) in pattern:
                    cols[col].button("💡", key=cell_key, help="Hint", use_container_width=True)
                elif (row, col) in selected_cells:
                    cols[col].button("🔵", key=cell_key, help="Selected", use_container_width=True)
                elif cols[col].button("⬜", key=cell_key, use_container_width=True):
                    new_selected_cells.append((row, col))
    
        return new_selected_cells

# Game Logic
    st.title("🎯 CalmSquares: Memory Challenge")

# Instructions
    st.markdown(
    """
    **Instructions:**  
    🧠 Memorize the green pattern when shown.  
    🔥 After a few seconds, recreate the pattern by clicking the correct squares.  
    💡 Use hints wisely (max 3 per game).
    """
    )

# Initialize game state
    if 'level' not in st.session_state:
        st.session_state['level'] = 1
    if 'grid_size' not in st.session_state:
        st.session_state['grid_size'], st.session_state['pattern_length'] = get_difficulty_settings(st.session_state['level'])
    if 'pattern' not in st.session_state:
        st.session_state['pattern'] = generate_pattern(st.session_state['grid_size'], st.session_state['pattern_length'])
        st.session_state['show_pattern'] = True
        st.session_state['score'] = 0
        st.session_state['selected_cells'] = []
        st.session_state['hints_used'] = 0
        st.session_state['leaderboard'] = []

    pattern = st.session_state['pattern']
    grid_size = st.session_state['grid_size']

# Show pattern with timer
    if st.session_state['show_pattern']:
        st.info("👀 Memorize this pattern...")
        display_grid(grid_size, pattern, reveal=True)
        time.sleep(3)
        st.session_state['show_pattern'] = False
        st.rerun()

# Display empty grid for user input
    st.success("🔥 Now recreate the pattern below!")
    st.session_state['selected_cells'] = display_grid(grid_size, selected_cells=st.session_state['selected_cells'])

# Hint functionality
    if st.session_state['hints_used'] < HINT_LIMIT:
        if st.button("🔍 Use Hint"):
            st.session_state['hints_used'] += 1
            display_grid(grid_size, pattern, hint=True)
            st.warning(f"Hint used! ({HINT_LIMIT - st.session_state['hints_used']} remaining)")

# Check result
    if st.button("🚀 Submit Pattern"):
        if set(st.session_state['selected_cells']) == set(pattern):
            st.success("✅ Correct! Level Up! 🎉")
            st.session_state['score'] += 10
            st.session_state['level'] += 1
            st.session_state['leaderboard'].append((st.session_state['score'], f"Level {st.session_state['level']}"))
            play_sound(True)
        else:
            st.error("❌ Incorrect. Try again!")
            play_sound(False)
            st.session_state['score'] = max(0, st.session_state['score'] - 5)

    # Increase difficulty and reset game state
        st.session_state['grid_size'], st.session_state['pattern_length'] = get_difficulty_settings(st.session_state['level'])
        st.session_state['pattern'] = generate_pattern(st.session_state['grid_size'], st.session_state['pattern_length'])
        st.session_state['show_pattern'] = True
        st.session_state['selected_cells'] = []

# Scoreboard and Leaderboard
    st.sidebar.markdown("<div class='score-badge'>🏅 Your Score: {}</div>".format(st.session_state['score']), unsafe_allow_html=True)
    st.sidebar.text(f"🚀 Level: {st.session_state['level']}")

# Leaderboard Display
    st.sidebar.title("📋 Leaderboard")
    for score, level in sorted(st.session_state['leaderboard'], reverse=True)[:5]:
        st.sidebar.markdown(f"<div class='leaderboard-badge'>{score} points - {level}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 



