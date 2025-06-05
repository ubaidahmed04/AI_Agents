import os
import json
import chainlit as cl
from dotenv import load_dotenv
from litellm import completion
import litellm
litellm._turn_on_debug()

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("APIKEY")

# Properly check API key
if not gemini_api_key:
    raise ValueError("❌ gemini_api_key is missing in .env")

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    await cl.Message(
        content=(
            "👋 Welcome to the **UA Agent By Ubaid**!\n\n"
            "Please tell me:\n"
            "- What you want to **translate**\n"
            "- Into which **language**"
        )
    ).send()
@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="🔄 Translating...")
    await msg.send()

    # Get or initialize chat history
    history = cl.user_session.get("chat_history") or []

    # Append current user message
    if not message.content.strip():
        msg.content = "⚠️ Please enter some text to translate."
        await msg.update()
        return

    history.append({"role": "user", "content": message.content})

    try:
        # Call LiteLLM completion API correctly
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=gemini_api_key,
            messages=history  # ✅ correct param name
        )

        response_content = response.choices[0].message.content

        # Update chat history
        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)

        msg.content = response_content
        await msg.update()

    except Exception as e:
        msg.content = f"❌ Error: {str(e)}"
        await msg.update()

@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("chat_history") or []
    with open("translation_chat_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print("✅ Chat history saved.")
