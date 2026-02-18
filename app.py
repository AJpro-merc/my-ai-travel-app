import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd

# --- 1. SAFE API CONFIGURATION (Using Secrets) ---
# This section fetches your keys from the Streamlit Cloud Dashboard
try:
    # IMPORTANT: Use these exact names in your Dashboard Secrets
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
except KeyError:
    st.error("❌ Missing API Keys in Streamlit Dashboard! Check your 'Secrets' settings.")
    st.stop()

# --- 2. CONFIGURE AI ---
# 'transport="rest"' fixes 404/Connection issues on Streamlit Cloud
genai.configure(api_key=GEMINI_API_KEY, transport="rest")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Voyager", page_icon="🌍", layout="wide")

# --- 3. DATA FUNCTIONS ---
def get_weather(city):
    # OpenWeather API call
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        r = requests.get(url).json()
        return {
            "temp": r['main']['temp'], 
            "desc": r['weather'][0]['description'], 
            "lat": r['coord']['lat'], 
            "lon": r['coord']['lon']
        }
    except Exception as e:
        st.error
