import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd

# --- API KEYS (Pulled from Streamlit Secrets) ---
try:
    GEMINI_API_KEY = st.secrets["AIzaSyCAJNQaeJY64OmCY1_bJrIDUOg0yYYukuM"]
    WEATHER_API_KEY = st.secrets["e77e109c4f7314b5d1e4bbb380d35170"]
except KeyError:
    st.error("Missing API Keys! Go to Streamlit Settings > Secrets and add them.")
    st.stop()

# Configure AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Voyager", page_icon="🌍", layout="wide")

# --- DATA FUNCTIONS ---
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

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.header("📍 Trip Settings")
    dest = st.text_input("Destination City", value="Tokyo")
    days = st.slider("Trip Duration (Days)", 1, 7, 3)
    budget = st.select_slider("Budget Level", options=["Budget", "Standard", "Luxury"])
    
    if st.button("Reset Adventure"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN APP ---
st.title(f"🌍 Journey to {dest}")

weather = get_weather(dest)

if weather:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Simple Map
        st.subheader("Map View")
        df = pd.DataFrame({'lat': [weather['lat']], 'lon': [weather['lon']]})
        st.map(df, zoom=10)
        st.metric("Current Weather", f"{weather['temp']}°C", weather['desc'])

    with col2:
        # Chat Interface
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if user_query := st.chat_input("Ask for an itinerary or tweak your plan..."):
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            with st.chat_message("assistant"):
                context = f"Plan a {days}-day {budget} trip to {dest}. Weather: {weather['desc']}. Request: {user_query}"
                response = model.generate_content(context)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})