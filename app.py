import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini 2.0 Flash API Endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Headers
headers = {
    "Content-Type": "application/json"
}

# Sarcastic Chatbot Response
def get_sarcastic_reply(user_input):
    payload = {
        "contents": [{
            "parts": [{"text": f"You are the 'Sarcastic Self-Help Guru'. Respond with wit and sarcasm to: {user_input}"}]
        }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="Sarcastic Self-Help Guru", page_icon="🧠")
st.title("🧠 Sarcastic Self-Help Guru")
st.caption("AI advice with a sprinkle of sass.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("What's your problem today?", placeholder="Try me... I dare you.")

if user_input:
    st.session_state.history.append(("You", user_input))
    with st.spinner("Generating backhanded wisdom..."):
        reply = get_sarcastic_reply(user_input)
        st.session_state.history.append(("Guru", reply))

for speaker, message in reversed(st.session_state.history):
    st.markdown(f"**{speaker}:** {message}")
