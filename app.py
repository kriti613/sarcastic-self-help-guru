import random
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from streamlit_chat import message


# ✅ ✅ ✅ Move this right after imports!
st.set_page_config(page_title="Sarcastic Self-Help Guru", page_icon="🧠")

# Custom Fonts and Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Comic Neue', cursive;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .animated-message {
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)




# Initialize chat history states
if "past" not in st.session_state:
    st.session_state["past"] = []

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a sarcastic self-help guru. Give witty, ironic advice with a touch of actual insight."}]



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
    emoji_list = ["😏", "🙄", "😂", "🤡", "😬", "🥴", "🫠", "💀"]
    selected_emoji = random.choice(emoji_list)

    payload = {
        "contents": [{
            "parts": [{"text": f"You are the 'Sarcastic Self-Help Guru'. Respond with wit, sarcasm, humor, and add emoji reactions. Input: {user_input}"}]
        }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return f"{selected_emoji} {reply}"
    else:
        return f"Error: {response.status_code} - {response.text}"


def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.history.append(("You", user_input))
        with st.spinner("Generating backhanded wisdom..."):
            reply = get_sarcastic_reply(user_input)
            st.session_state.history.append(("Guru", reply))
        # ✅ Now safely clear input inside the callback
        st.session_state.user_input = ""



def render_chat_pair(pair):
    user_message = f"""
    <div style='display: flex; justify-content: flex-end; margin: 10px 0;'>
        <div style='max-width: 60%; background-color: #6c5ce7; color: white; padding: 10px 15px; border-radius: 15px;'>
            <strong>🧑 You:</strong><br>{pair['user']}
        </div>
    </div>
    """

    guru_message = f"""
    <div style='display: flex; justify-content: flex-start; margin: 5px 0 15px 0;'>
        <div style='max-width: 60%; background-color: #00cec9; color: black; padding: 10px 15px; border-radius: 15px;'>
            <strong>🤖 Guru:</strong><br>{pair['guru']}
        </div>
    </div>
    """

    st.markdown(user_message + guru_message, unsafe_allow_html=True)




# Streamlit UI
# st.set_page_config(page_title="Sarcastic Self-Help Guru", page_icon="🧠")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

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



st.markdown("""
    <style>
    .sample-button button {
        width: 100%;
        height: 60px;
        border-radius: 8px;
        font-size: 14px;
        padding: 8px 12px;
        white-space: normal; /* Allow text to wrap */
        word-break: break-word;
        text-align: center;
    }

    .sample-button {
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)


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
                st.session_state["past"].append(question)
                with st.spinner("Guru is crafting your roast..."):
                    reply = get_sarcastic_reply(question)
                st.session_state["generated"].append(reply)
                st.session_state["messages"].append({"role": "user", "content": question})
                st.session_state["messages"].append({"role": "assistant", "content": reply})
            st.markdown("</div>", unsafe_allow_html=True)







# Session State Initialization
if "history" not in st.session_state:
    st.session_state.history = []


if "user_input" not in st.session_state:
    st.session_state.user_input = ""


# user_input = st.chat_input("What's your tragic tale today?")

# Define dynamic placeholder texts
placeholders = [
    "What's your tragic tale today? 😅",
    "Give me a reason to roll my eyes 🙄",
    "Feeling existential? Vent here...",
    "Need brutal honesty? I'm ready. 🤡",
    "Confess your questionable choices 💀",
    "What mess are we cleaning up today? 🧹"
]

user_input = st.chat_input(random.choice(placeholders))




# ✅ Process manual user input (this is what was missing!)
if user_input:
    st.session_state["past"].append(user_input)
    with st.spinner("Guru is crafting your roast..."):
        reply = get_sarcastic_reply(user_input)
    st.session_state["generated"].append(reply)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["messages"].append({"role": "assistant", "content": reply})


if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"])):
        if i < len(st.session_state["past"]):
            # message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(
    f"<div class='animated-message'>{st.session_state['past'][i]}</div>",
    is_user=True,
    key=str(i) + "_user",
    allow_html=True
)

        # message(st.session_state["generated"][i], key=str(i))
        message(
    f"<div class='animated-message'>{st.session_state['generated'][i]}</div>",
    key=str(i),
    allow_html=True
)





def handle_input():
    user_input = st.session_state.user_input
    if user_input:

        st.session_state.history.append(("You", user_input))
        
        with st.spinner("Generating backhanded wisdom..."):
            reply = get_sarcastic_reply(user_input)
            st.session_state.history.append(("Guru", reply))
        # ✅ Now safely clear input inside the callback
        st.session_state.user_input = ""
