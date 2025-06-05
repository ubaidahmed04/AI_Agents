import streamlit as st
import os
from dotenv import load_dotenv
from litellm import completion
import litellm
import json

# Debug logs for LiteLLM
litellm._turn_on_debug()

# Load environment variable
load_dotenv()
gemini_api_key = os.getenv("APIKEY")

# Check for API key
if not gemini_api_key:
    st.error("❌ API key not found. Please check your .env file.")
    st.stop()

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.set_page_config(page_title="UA Agent by Ubaid", layout="centered")
st.title("🌐 UA Agent by Ubaid")
st.markdown("Enter text below and select the language to translate to.")

# Input form
with st.form(key="translate_form"):
    user_input = st.text_area("✏️ Text to Translate", height=150)
    target_language = st.text_input("🌍 Target Language (e.g., Urdu, Spanish)")
    submitted = st.form_submit_button("🔄 Translate")

# Process submission
if submitted:
    if not user_input.strip() or not target_language.strip():
        st.warning("⚠️ Please provide both text and target language.")
    else:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": f"Translate this into {target_language}: {user_input}"})

        try:
            response = completion(
                model="gemini/gemini-1.5-flash",
                api_key=gemini_api_key,
                messages=st.session_state.chat_history,
            )

            translated_text = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": translated_text})

            st.success("✅ Translation:")
            st.markdown(f"**{translated_text}**")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Option to export chat history
if st.button("💾 Save Chat History"):
    with open("translation_chat_history.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_history, f, indent=2, ensure_ascii=False)
    st.success("✅ Chat history saved.")
