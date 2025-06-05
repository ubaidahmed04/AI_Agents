from dotenv import load_dotenv
import os
from agents import Agent, Runner ,AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

load_dotenv()
gemini_api_key= os.getenv("APIKEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


agent = Agent(name="Assistant", instructions="You are a helpful assistant. Always Translate English sentences onto simple Urdu ")

result = Runner.run_sync(agent, 
                         "I am frontend Developer",
                         run_config=config)
print(result.final_output)