import os
from glob import glob
from typing import Dict, List

import gradio as gr
import requests
from openai import OpenAI
from openrouter import OpenRouter
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

def load_skills_index() -> str:
    skills = []
    for path in sorted(glob("skills/*/SKILL.md")):
        name = description = ""
        in_frontmatter = False
        with open(path) as f:
            for line in f:
                line = line.rstrip()
                if line == "---":
                    in_frontmatter = not in_frontmatter
                    continue
                if in_frontmatter:
                    if line.startswith("name:"):
                        name = line.split(":", 1)[1].strip()
                    elif line.startswith("description:"):
                        description = line.split(":", 1)[1].strip()
                if name and description:
                    break
        if name:
            skills.append(f"- {name}: {description}")

    index = "Available skills:\n" + "\n".join(skills)
    index += "\n\nTo use a skill, first read its full details with: Execute command: cat skills/<skill_name>/SKILL.md"
    return index


messages: List[Dict[str, str]] = [
    {
        "role": "system",
        "content": open("agent.md").read() + "\n\n" + load_skills_index(),
    }
]


def call_model(message: str, model: str = "", provider: str = "claude") -> str:
    if provider == "claude":
        return greet_claude(message)
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


def greet_ollama(message: str, model: str = "qwen2.5-coder:3b") -> str:
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
            break
        command = res.strip().split("Execute command:")[1].strip()
        command_result = os.popen(command).read()
        print(f"[Command Result] {command_result}")
        messages.append({"role": "user", "content": command_result})
    # shut down local ollama llm instance
    unload_model(model)
    return res

def greet_claude(message: str) -> str:
    async def _run():
        nonlocal message
        while True:
            messages.append({"role": "user", "content": message})

            # Build conversation string for stateless query
            prompt = "\n".join(
                f"{m['role'].upper()}: {m['content']}"
                for m in messages[1:]
            )

            res = ""
            async for msg in query(
                prompt=prompt,
                options=ClaudeAgentOptions(
                    cwd=".",
                    system_prompt=messages[0]["content"],
                    allowed_tools=["Read", "Write", "Bash"],
                    max_turns=1,
                ),
            ):
                print(f"[MSG type={type(msg).__name__}] {msg}")
                if isinstance(msg, ResultMessage):
                    res = msg.result

            messages.append({"role": "assistant", "content": res})
            print(f"[AI] {res}")
            if res.strip().startswith("Finished:"):
                break
            if "Execute command:" not in res:
                print(f"[Warning] Unexpected response: {res}")
                break
            command = res.strip().split("Execute command:")[1].strip()
            command_result = os.popen(command).read()
            print(f"[Command Result] {command_result}")
            message = command_result
        return res
    return anyio.run(_run)



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
        fn=greet_claude,
        inputs=["text"],
        outputs=["text"],
        api_name="predict",
    )

    demo.launch()
