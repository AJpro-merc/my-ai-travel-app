# --- 1. SAFE API CONFIGURATION ---
try:
    # Use these EXACT names in your Streamlit Secrets dashboard
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
except KeyError:
    st.error("Error: Key names in Streamlit Secrets do not match the code.")
    st.stop()

# --- 2. CONFIGURE AI WITH TRANSPORT FIX ---
genai.configure(api_key=GEMINI_API_KEY, transport="rest")
model = genai.GenerativeModel('gemini-1.5-flash')
