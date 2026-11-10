from langchain_ollama import ChatOllama
from huggingface_hub import InferenceClient
from config import Settings
from langchain.agents import create_agent

settings = Settings()

def get_ollama_llm(model = "qwen3:1.7b", temperature = 0):
    llm = ChatOllama(
        model = model,
        temprature = temperature
    )
    return llm

def get_inference_client(api_key = ""):
    if api_key == "":
        api_key = settings.HF_TOKEN
        if not api_key:
            raise ValueError("API key is required")
    return InferenceClient(api_key = api_key)

def get_inference_chat_client(client, model, content):
    completion = client.chat.completions.create(
        model = model,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
    )
    return completion.choices[0].message.content

def get_agent(llm, prompt):
    agent = create_agent(
        model = llm,
        system_prompt= prompt
    )
    return agent