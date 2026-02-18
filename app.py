import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd

# --- 1. INITIALIZE SESSION STATE FIRST ---
# This prevents "NameError" or "AttributeError"
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. SAFE API CONFIGURATION ---
try:
    # These must match your labels in the Streamlit Secrets dashboard
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
except Exception as e:
    st.error(f"❌ Secrets Error: {e}. Go to Settings > Secrets and check your labels.")
    st.stop()

# --- 3. CONFIGURE AI ---
# transport="rest" fixes common 404/connection errors
try:
    genai.configure(api_key=GEMINI_API_KEY, transport="rest")
    # Using 'gemini-1.5-flash' - ensure no extra spaces
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
