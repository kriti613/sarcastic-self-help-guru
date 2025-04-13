import streamlit as st
import google.generativeai as genai
import os

# Set up your Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Sarcastic Self-Help Guru", page_icon="🧠")
st.title("🧠 Sarcastic Self-Help Guru")
st.caption("The only guru who tells it how it *really* is.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("What’s bothering you today?", placeholder="Type your tragedy here...")

if user_input:
    st.session_state.history.append(("You", user_input))
    with st.spinner("Rolling eyes... I mean, thinking..."):
        response = model.generate_content(
            f"You are a sarcastic self-help chatbot. Someone just said: '{user_input}'. Give them advice that's dripping in sarcasm, but deep down, strangely helpful."
        )
        reply = response.text
        st.session_state.history.append(("Guru", reply))

# Display chat history
for speaker, message in st.session_state.history[::-1]:
    st.markdown(f"**{speaker}:** {message}")
