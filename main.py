import os
from typing import Dict, List

import gradio as gr
import requests
from openai import OpenAI
from openrouter import OpenRouter

messages: List[Dict[str, str]] = [
    {
        "role": "system",
        "content": open("agent.md").read(),
    }
]

def call_model(message: str, model: str, provider: str = "ollama") -> str:
    if provider == "ollama":
        return greet_ollama(message, model)
    elif provider == "openrouter":
        return greet_world(message, model)
    else:
        return f"Unknown provider: {provider}"


def ensure_model_exists(model: str):
    tags = requests.get("http://localhost:11434/api/tags").json()

    models = [m["name"] for m in tags.get("models", [])]
    if model not in models:
        print(f"Model {model} not found. Pulling...")
        requests.post(
            "http://localhost:11434/api/pull",
            json={"name": model},
        )


def unload_model(model: str):
    requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": "",
            "keep_alive": 0,
        },
    )


def greet_ollama(message: str, model: str = "llama3") -> str:
    ensure_model_exists(model)
    # check local allama server start a llm instance based on model parameter
    while True:
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        res = response.choices[0].message.content
        messages.append({"role": "assistant", "content": res})
        print(f"[AI] {res}")
        if res.strip().startswith("Finished:"):
            print("[AI] Task finished.")
            break
        command = res.strip().split("Execute command:")[1].strip()
        command_result = os.popen(command).read()
        print(f"[Command Result] {command_result}")
        messages.append({"role": "user", "content": command_result})
    # shut down local ollama llm instance
    unload_model(model)
    return res


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
        fn=greet_ollama,
        inputs=["text"],
        outputs=["text"],
        api_name="predict",
    )

    demo.launch()
