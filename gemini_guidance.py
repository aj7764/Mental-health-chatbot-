import google.generativeai as genai
import random

# ---- 🌐 Gemini AI API Key ----
GEMINI_API_KEY = "AIzaSyCZdn5mTxJKgdLtP-DGPa6KvSJWuNDeazs"
genai.configure(api_key=GEMINI_API_KEY)

# List of prompts for varied responses
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
    """Generate text-based breathing guidance from Gemini AI."""
    prompt = random.choice(PROMPTS)  # Select a random prompt
    try:
        response = genai.chat(messages=[{"role": "user", "content": prompt}])
        return response.text
    except Exception:
        return "Breathe in... Hold... Breathe out... Relax."
