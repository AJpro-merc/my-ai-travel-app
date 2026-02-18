import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd

# --- 1. SAFE API CONFIGURATION (Using Secrets) ---
try:
    # Use these EXACT labels in your Streamlit Secrets dashboard
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
except KeyError:
    st.error("Missing API Keys! Go to Streamlit Settings > Secrets and add them.")
    st.stop()

# --- 2. CONFIGURE AI ---
# transport="rest" fixes connection hanging and 404 errors on some hosting platforms
genai.configure(api_key=GEMINI_API_KEY, transport="rest")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Voyager", page_icon="🌍", layout="wide")

# --- 3. DATA FUNCTIONS ---
def get_
