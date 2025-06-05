import streamlit as st
import os
from dotenv import load_dotenv
from litellm import completion
import litellm
import json

# Enable debugging logs
litellm._turn_on_debug()

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("APIKEY")

if not gemini_api_key:
    st.error("❌ API key not found. Please check your .env file.")
    st.stop()

# Set page config
st.set_page_config(page_title="UA Agent Chat", layout="centered")
st.title("🧠 UA Translator Chatbot by Ubaid")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box like ChatGPT
user_prompt = st.chat_input("✏️ Ask me to translate something...")

if user_prompt:
    user_message = f"Translate this into the target language: {user_prompt}"
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        # Send request to LiteLLM/Gemini
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=gemini_api_key,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history
            ],
        )

        assistant_reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.error(error_msg)

# Save history button
with st.sidebar:
    if st.button("💾 Save Chat History"):
        with open("translation_chat_history.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state.chat_history, f, indent=2, ensure_ascii=False)
        st.success("✅ Chat history saved.")
