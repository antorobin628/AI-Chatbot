import streamlit as st
import sys
import os

# Add backend path
sys.path.append(os.path.join(os.getcwd(), "Backend"))
from Chatbot import ChatBot
from SpeechToText import get_speech_text

# ---- Page Config ----
st.set_page_config(page_title="ChatBot-1ne", layout="wide")

# ---- Custom Styling ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f5f7fa;
        color: #333;
    }

    .title {
        text-align: center;
        font-size: 3em;
        font-weight: 600;
        color: #394867;
        margin-bottom: 1rem;
    }

    .chat-bubble {
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border-radius: 1.5rem;
        max-width: 80%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        font-size: 1.05rem;
        line-height: 1.5;
    }

    .user {
        background-color: #d1e7dd;
        align-self: flex-end;
        margin-left: auto;
    }

    .bot {
        background-color: #e2e3e5;
        align-self: flex-start;
        margin-right: auto;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
        margin: 2rem auto;
        width: 70%;
    }

    .stButton > button {
        background-color: #3f72af;
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 0.5rem;
        font-size: 1rem;
        border: none;
        transition: all 0.3s ease;
        margin: 0.25rem 0.5rem 1rem 0;
    }

    .stButton > button:hover {
        background-color: #2c5282;
        transform: scale(1.02);
    }

    .stTextInput > div > input {
        font-size: 1.1rem;
        padding: 0.75rem;
        border: 1px solid #ccc;
        border-radius: 0.5rem;
    }

    </style>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown('<div class="title">ChatBot-1ne</div>', unsafe_allow_html=True)

# ---- Chat History ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- User Input ----
query = st.text_input("💬 Type your message or click Speak:", "")

# ---- Speak Button ----
col1, col2 = st.columns([1, 6])
with col1:
    if st.button("🎤 Speak"):
        with st.spinner("Listening..."):
            try:
                spoken_query = get_speech_text()
                st.success(f"🗣️ You said: {spoken_query}")
                query = spoken_query
            except Exception as e:
                st.error(f"❌ Speech recognition failed: {e}")

# ---- Send Button ----
with col2:
    if st.button("🚀 Send"):
        if query.strip():
            answer = ChatBot(query)
            st.session_state.chat_history.append(("You", query))
            st.session_state.chat_history.append(("Bot", answer))
            st.experimental_rerun()

# ---- Show Conversation ----
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, msg in st.session_state.chat_history:
    role_class = "user" if sender == "You" else "bot"
    st.markdown(
        f'<div class="chat-bubble {role_class}"><strong>{sender}:</strong><br>{msg}</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)
