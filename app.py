import streamlit as st
import time
import json
import random
import google.generativeai as genai
import traceback

# ---- 🌐 Gemini AI API Key ----
GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

# ---- 🎨 PAGE CONFIGURATION ----
st.set_page_config(page_title="🌬️ Breathing Bubble Pop", layout="wide")

# ---- 🌈 CUSTOM STYLES ----
st.markdown("""
    <style>
        html, body, .main {
            height: 100%;
            background: linear-gradient(to bottom right, #cce2ff, #e0ffe9);
            font-family: 'Segoe UI', sans-serif;
            color: #1e293b;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 50vh;
        }
        .bubble {
            width: 200px;
            height: 200px;
            background: radial-gradient(circle at center, #FFDEE9, #B5FFFC);
            border-radius: 50%;
            animation: pulse 4s infinite;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.3);
        }
        @keyframes pulse {
            0% { transform: scale(0.8); opacity: 0.6; }
            50% { transform: scale(1.5); opacity: 1; }
            100% { transform: scale(0.8); opacity: 0.6; }
        }
        .progress-container {
            text-align: center;
            margin-top: 30px;
        }
        .progress-bar {
            width: 80%;
            height: 20px;
            background: linear-gradient(to right, #84fab0, #8fd3f4);
            border-radius: 10px;
            animation: progressAnimation 3s infinite alternate;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        @keyframes progressAnimation {
            from { width: 20%; }
            to { width: 80%; }
        }
        .play-button {
            background: linear-gradient(to right, #f6d365, #fda085);
            padding: 15px;
            border-radius: 12px;
            color: #1f2937;
            font-size: 16px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .play-button:hover {
            background: linear-gradient(to right, #f093fb, #f5576c);
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# ---- 🎙 TEXT-BASED GUIDANCE (Gemini AI) ----
PROMPTS = [
    "Guide a relaxing deep breathing session for stress relief.",
    "Provide a slow-paced breathing exercise for mindfulness.",
    "Describe a calming breath technique for anxiety reduction.",
    "Give step-by-step instructions for a breathing meditation.",
    "Offer a soothing breath practice for relaxation and focus.",
    "Create a short breathing exercise to help with sleep.",
    "Generate a breathing routine inspired by yoga and meditation."
]

def get_gemini_guidance():
    import traceback
    prompt = random.choice(PROMPTS)
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        response = model.generate_content(prompt)

        return response.text

    except Exception:
        error_msg = traceback.format_exc()
        print("❌ Gemini Error Traceback:\n", error_msg) 
        st.error("❌ Gemini API Error occurred. Full traceback below:")
        st.code(error_msg)
        return "Breathe in... Hold... Breathe out... Relax."

# ---- 📊 PROGRESS TRACKING ----
PROGRESS_FILE = "progress.json"

try:
    with open(PROGRESS_FILE, "r") as file:
        progress_data = json.load(file)
except FileNotFoundError:
    progress_data = {"breaths_taken": 0}

def save_progress():
    with open(PROGRESS_FILE, "w") as file:
        json.dump(progress_data, file)

# ---- 🚀 UI CONTENT ----
st.markdown("<h1 style='text-align: center; color: #4f46e5;'>🌬️ Breathing Bubble Pop</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Follow the bubble. Inhale as it grows, exhale as it pops.</p>", unsafe_allow_html=True)

st.markdown('<div class="container"><div class="bubble"></div></div>', unsafe_allow_html=True)

st.markdown("### 🎈 How to Play")
st.markdown("<div class='instructions'>Inhale deeply as the bubble grows, hold as it peaks, and exhale as it shrinks.</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<button class="play-button">1️⃣ Inhale for 4 seconds 🌬️</button>', unsafe_allow_html=True)
with col2:
    st.markdown('<button class="play-button">2️⃣ Hold for 7 seconds ⏳</button>', unsafe_allow_html=True)
with col3:
    st.markdown('<button class="play-button">3️⃣ Exhale for 8 seconds 💨</button>', unsafe_allow_html=True)

st.write("✨ **Repeat this cycle to relax and feel at peace.** 🧘‍♀️")

# ---- 🌟 PROGRESS SECTION ----
st.markdown("### 🌟 Your Progress")
progress = min(100, (progress_data["breaths_taken"] % 10) * 10)
st.markdown('<div class="progress-container"><div class="progress-bar"></div></div>', unsafe_allow_html=True)
st.write(f"Total breaths taken: **{progress_data['breaths_taken']}**")

# ---- 📣 GUIDANCE ----
if st.button("💬 Get Breathing Guidance"):
    guidance = get_gemini_guidance()
    st.success(guidance)

# ---- 🧘 BREATHING CYCLES ----
for cycle in range(3):
    st.write(f"**Cycle {cycle + 1}: Inhale...** 🌿")
    time.sleep(4)
    st.write("**Hold your breath...** ⏳")
    time.sleep(7)
    st.write("**Exhale slowly...** 🎈💨")
    time.sleep(8)
    progress_data["breaths_taken"] += 1
    save_progress()

# ---- 🎉 MOTIVATION ----
motivations = [
    "You're doing great! 🌟",
    "Keep going, your mind is relaxing. 🧘",
    "Breathe deeply, feel the calm. 🍃",
    "One breath at a time, you're in control. 💙",
]
st.success(motivations[progress_data["breaths_taken"] % len(motivations)])

st.success("💙 You did great! Repeat as needed for relaxation.")
