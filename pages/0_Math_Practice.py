import streamlit as st
import random
import time
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Math Practice",
    page_icon="🧮",
    layout="centered"
)

# File to store user progress
PROGRESS_FILE = "user_progress.json"

def load_progress():
    """Load user progress from file"""
    try:
        if Path(PROGRESS_FILE).exists():
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_progress(name, difficulty):
    """Save user progress to file"""
    try:
        progress = load_progress()
        progress[name] = difficulty
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f)
    except:
        pass

def generate_question(difficulty):
    """Generate a math question based on difficulty level"""
    max_num = 10 + int(difficulty * 5)
    
    # Choose question type randomly
    question_type = random.choice(['a+x=b', 'a+b=x', 'x-a=b', 'a-x=b'])
    
    if question_type == 'a+x=b':
        a = random.randint(1, max_num)
        x = random.randint(1, max_num)
        b = a + x
        question = f"{a} + ? = {b}"
        answer = x
    elif question_type == 'a+b=x':
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        x = a + b
        question = f"{a} + {b} = ?"
        answer = x
    elif question_type == 'x-a=b':
        b = random.randint(1, max_num)
        a = random.randint(1, max_num)
        x = a + b  # Ensure x > a for positive result
        question = f"? - {a} = {b}"
        answer = x
    else:  # 'a-x=b'
        a = random.randint(max(10, max_num), max_num + 10)
        b = random.randint(1, a - 1)  # Ensure positive result
        x = a - b
        question = f"{a} - ? = {b}"
        answer = x
    
    return question, answer

def init_session_state():
    """Initialize session state variables"""
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 0
    if 'correct_count' not in st.session_state:
        st.session_state.correct_count = 0
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = 1
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    if 'user_was_correct' not in st.session_state:
        st.session_state.user_was_correct = False
    if 'show_stats' not in st.session_state:
        st.session_state.show_stats = False
    if 'total_time' not in st.session_state:
        st.session_state.total_time = 0

def start_game():
    """Start or restart the game"""
    st.session_state.game_active = True
    st.session_state.question_count = 0
    st.session_state.correct_count = 0
    st.session_state.start_time = time.time()
    st.session_state.show_result = False
    st.session_state.show_stats = False
    generate_new_question()

def generate_new_question():
    """Generate a new question"""
    question, answer = generate_question(st.session_state.difficulty)
    st.session_state.current_question = question
    st.session_state.current_answer = answer
    st.session_state.show_result = False

def check_answer(user_answer):
    """Check if the user's answer is correct"""
    if user_answer == st.session_state.current_answer:
        st.session_state.correct_count += 1
        st.session_state.difficulty += 0.2  # Gradually increase difficulty
        st.session_state.user_was_correct = True
    else:
        st.session_state.user_was_correct = False
    
    st.session_state.question_count += 1
    st.session_state.show_result = True
    
    # Check if we've completed 10 questions
    if st.session_state.question_count >= 10:
        st.session_state.total_time = time.time() - st.session_state.start_time
        st.session_state.show_stats = True
        st.session_state.game_active = False
        save_progress(st.session_state.name, st.session_state.difficulty)

def continue_game():
    """Continue playing after stats"""
    st.session_state.question_count = 0
    st.session_state.correct_count = 0
    st.session_state.start_time = time.time()
    st.session_state.show_stats = False
    st.session_state.game_active = True
    generate_new_question()

def end_game():
    """End the game completely"""
    st.session_state.game_active = False
    st.session_state.show_stats = False
    st.session_state.name = ""

# Initialize session state
init_session_state()

# Main app
st.title("🧮 Math Practice Game")

# Name input (if not set)
if not st.session_state.name:
    st.write("Welcome! Let's practice some math!")
    name_input = st.text_input("What's your name?", key="name_input")
    
    if st.button("Start Playing") and name_input:
        st.session_state.name = name_input
        # Check if user has previous progress
        progress = load_progress()
        if name_input in progress:
            st.session_state.difficulty = progress[name_input]
            st.success(f"Welcome back, {name_input}! Continuing from difficulty level {int(st.session_state.difficulty)}")
        else:
            st.success(f"Welcome, {name_input}! Let's start with some easy questions.")
        start_game()
        st.rerun()

# Game is active
elif st.session_state.game_active and not st.session_state.show_stats:
    st.write(f"### Player: {st.session_state.name}")
    st.write(f"**Question {st.session_state.question_count + 1} of 10** | Difficulty Level: {int(st.session_state.difficulty)}")
    st.write(f"Correct Answers: {st.session_state.correct_count}/{st.session_state.question_count}")
    
    st.divider()
    
    # Show current question
    st.write(f"## {st.session_state.current_question}")
    
    # Show result of previous answer if applicable
    if st.session_state.show_result:
        if st.session_state.user_was_correct:
            st.success("✅ Correct! Great job!")
        else:
            st.error(f"❌ Incorrect. The answer was {st.session_state.current_answer}")
        
        if st.button("Next Question"):
            generate_new_question()
            st.rerun()
    else:
        # Input for answer
        user_answer = st.number_input("Your answer:", min_value=0, step=1, key=f"answer_{st.session_state.question_count}")
        
        if st.button("Submit Answer"):
            check_answer(user_answer)
            st.rerun()

# Show stats after 10 questions
elif st.session_state.show_stats:
    st.write(f"### Great job, {st.session_state.name}! 🎉")
    st.divider()
    
    st.metric("Correct Answers", f"{st.session_state.correct_count}/10")
    st.metric("Time Taken", f"{st.session_state.total_time:.1f} seconds")
    st.metric("Accuracy", f"{st.session_state.correct_count * 10}%")
    st.metric("Current Difficulty Level", f"{int(st.session_state.difficulty)}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play 10 More Questions"):
            continue_game()
            st.rerun()
    with col2:
        if st.button("End Game"):
            end_game()
            st.rerun()

# Footer
st.divider()
st.caption("Built with Streamlit 🚀")