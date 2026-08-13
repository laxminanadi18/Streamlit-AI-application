
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ==========================================
# Load API Key from .env
# ==========================================
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

# Check API key
if not api_key:
    st.error("❌ OPENROUTER_API_KEY not found in .env file.")
    st.stop()

# ==========================================
# OpenRouter Client
# ==========================================
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="My Chatbot for project",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# Sidebar
# ==========================================
with st.sidebar:

    st.title("🤖 My Chatbot for project")

    st.write("Chat with an AI assistant.")

    model = st.selectbox(
        "Choose AI Model",
        [
            "openai/gpt-4o-mini",
            "openai/gpt-4o",
            "openai/gpt-4.1-mini"
        ]
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by OpenRouter + OpenAI API")

# ==========================================
# Main Page
# ==========================================
st.title("💬 My Chatbot for project")
st.caption("Ask questions, learn concepts, write code, and more.")

# ==========================================
# Initialize Chat History
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# Display Chat History
# ==========================================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# User Input
# ==========================================
prompt = st.chat_input("Message AI...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful AI assistant. "
                                "Give clear, accurate and easy-to-understand answers."
                            )
                        }
                    ] + st.session_state.messages
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"❌ Error: {str(e)}")
