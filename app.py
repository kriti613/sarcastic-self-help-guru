import random
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from streamlit_chat import message

# ====== Setup ======
st.set_page_config(page_title="Sarcastic Self-Help Guru", page_icon="🧠")

# ====== Styling ======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Comic Neue', cursive;
    }
    .animated-message {
        animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .sample-button button {
        width: 100%;
        height: 60px;
        border-radius: 8px;
        font-size: 14px;
        padding: 8px 12px;
        white-space: normal;
        word-break: break-word;
        text-align: center;
    }
    .sample-button {
        padding: 5px;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ====== Initialize Session State ======
if "past" not in st.session_state:
    st.session_state["past"] = []

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a sarcastic self-help guru. Give witty, ironic advice with a touch of actual insight."}]

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# ====== Load API Key ======
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# ====== API Call Function ======
def get_sarcastic_reply(user_input):
    emoji_list = ["😏", "🙄", "😂", "🤡", "😬", "🥴", "🫠", "💀"]
    selected_emoji = random.choice(emoji_list)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are the 'Sarcastic Self-Help Guru'. Respond with wit, sarcasm, humor, and add emoji reactions. Make your response 3-4 lines. Input: {user_input}"
            }]
        }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return f"{selected_emoji} {reply}"
    else:
        return f"Error: {response.status_code} - {response.text}"

# ====== UI Headings ======
st.title("🧠 Sarcastic Self-Help Guru")
st.caption("AI advice with a sprinkle of sass.")

welcome_messages = [
    "Welcome back to your daily dose of disappointment. 😏",
    "Let's pretend this will help you. 🫠",
    "Brace yourself, questionable advice incoming. 🤡",
    "You've made worse choices, so let's chat. 💀",
    "Sarcasm loading... hope you're emotionally prepared. 😂",
    "Because therapy is expensive, and I'm free. 🙄"
]
st.markdown(f"<h3 style='text-align: center;'>{random.choice(welcome_messages)}</h3>", unsafe_allow_html=True)

# ====== Sample Questions ======
if not st.session_state["generated"]:
    st.markdown("#### 💡 Sample Questions to get roasted on:")
    cols = st.columns(3)
    sample_questions = [
        "How to not hate my life?",
        "Why am I always broke?",
        "Is my crush into me?",
    ]
    for col, question in zip(cols, sample_questions):
        with col:
            st.markdown("<div class='sample-button'>", unsafe_allow_html=True)
            if st.button(question, key=question):
                with st.spinner("Guru is crafting your roast..."):
                    reply = get_sarcastic_reply(question)
                st.session_state["past"].append(question)
                st.session_state["generated"].append(reply)
                st.session_state["messages"].append({"role": "user", "content": question})
                st.session_state["messages"].append({"role": "assistant", "content": reply})
            st.markdown("</div>", unsafe_allow_html=True)

# ====== Custom User Input ======
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Your tragic tale:", placeholder="Type here... 😏")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    with st.spinner("Guru is crafting your roast..."):
        reply = get_sarcastic_reply(user_input)
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(reply)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# ====== Display Chat ======
if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"])):
        if i < len(st.session_state["past"]):
            message(
                f"<div class='animated-message'>{st.session_state['past'][i]}</div>",
                is_user=True,
                key=str(i) + "_user",
                allow_html=True
            )
        message(
            f"<div class='animated-message'>{st.session_state['generated'][i]}</div>",
            key=str(i),
            allow_html=True
        )
