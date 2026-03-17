import os

import gradio as gr
import requests
from openai import OpenAI
from openrouter import OpenRouter

def call_model(message: str, model: str, provider: str = "ollama") -> str:
    if provider == "ollama":
        return greet_ollama(message, model)
    elif provider == "openrouter":
        return greet_world(message, model)
    else:
        return f"Unknown provider: {provider}"

def ensure_model_exists(model: str):
    """
    確保模型存在（沒有就 pull）
    """
    tags = requests.get("http://localhost:11434/api/tags").json()

    models = [m["name"] for m in tags.get("models", [])]
    if model not in models:
        print(f"Model {model} not found. Pulling...")
        requests.post(
            "http://localhost:11434/api/pull",
            json={"name": model},
        )


def unload_model(model: str):
    """
    卸載模型（釋放記憶體）
    """
    requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": "",
            "keep_alive": 0,  # 🔥 關鍵：立即 unload
        },
    )


def greet_ollama(message: str, model: str = "llama3") -> str:
    ensure_model_exists(model)
    # check local allama server start a llm instance based on model parameter
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )
    response = client.chat.completions.create(
        model=model,  # 換成你本地模型
        messages=[{"role": "user", "content": message}],
    )
    # shut down local ollama llm instance
    unload_model(model)
    return response.choices[0].message.content


def greet_world(message: str, model: str = "minimax/minimax-m2") -> str:
    try:
        with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
            response = client.chat.send(
                model=model, messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    demo = gr.Interface(
        fn=call_model, inputs=["text", "text", "text"], outputs=["text"], api_name="predict"
    )

    demo.launch()
