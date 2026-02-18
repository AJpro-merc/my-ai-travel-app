import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd

# --- 1. SAFE API CONFIGURATION (Using Secrets) ---
try:
    # These labels must match exactly what you type in Streamlit Dashboard Secrets
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
except KeyError:
    st.error("Missing API Keys! Go to Streamlit Settings > Secrets and add them.")
    st.stop()

# --- 2. CONFIGURE AI ---
# transport="rest" fixes connection hanging issues on Streamlit Cloud
genai.configure(api_key=GEMINI_API_KEY, transport="rest")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Voyager", page_icon="🌍", layout="wide")

# --- 3. DATA FUNCTIONS ---
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        r = requests.get(url).json()
        return {
            "temp": r['main']['temp'], 
            "desc": r['weather'][0]['description'], 
            "lat": r['coord']['lat'], 
            "lon": r['coord']['lon']
        }
    except:
        return None

# --- 4. SESSION STATE (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("📍 Trip Settings")
    dest = st.text_input("Destination City", value="Tokyo")
    days = st.slider("Trip Duration (Days)", 1, 7, 3)
    budget = st.select_slider("Budget Level", options=["Budget", "Standard", "Luxury"])
    
    if st.button("Reset Adventure"):
        st.session_state.messages = []
        st.rerun()

# --- 6. MAIN APP INTERFACE ---
st.title(f"🌍 Journey to {dest}")

weather = get_weather(dest)

if weather:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Map View")
        df = pd.DataFrame({'lat': [weather['lat']], 'lon': [weather['lon']]})
        st.map(df, zoom=10)
        st.metric("Current Weather", f"{weather['temp']}°C", weather['desc'])

    with col2:
        # Display chat history
        for msg in st.session_state.
