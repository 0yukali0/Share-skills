import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import flyte

env = flyte.TaskEnvironment(name="mindmap_env")


def gen_mindmap_mermaid(topic: str, items: list) -> str:
    """Generate Mermaid mindmap syntax from a topic and structured items.

    Args:
        topic: Root node text for the mindmap.
        items: List of strings or nested dicts representing child nodes.
            - str: becomes a direct child node
            - dict: keys become child nodes, values (list) become their children

    Returns:
        A valid Mermaid mindmap syntax string.
    """
    lines = ["mindmap", f"  {topic}"]

    def _add_items(items_list: list, depth: int = 2):
        indent = "  " * depth
        for item in items_list:
            if isinstance(item, str):
                lines.append(f"{indent}{item}")
            elif isinstance(item, dict):
                for key, children in item.items():
                    lines.append(f"{indent}{key}")
                    if isinstance(children, list):
                        _add_items(children, depth + 1)

    _add_items(items)
    return "\n".join(lines)


def mermaid_to_png(mermaid_code: str, output_path: str) -> str:
    """Convert Mermaid syntax string to a PNG image file using mmdc.

    Args:
        mermaid_code: Valid Mermaid syntax string.
        output_path: File path for the output PNG image.

    Returns:
        The absolute path of the generated PNG file.

    Raises:
        FileNotFoundError: If mmdc (mermaid-cli) is not installed.
        subprocess.CalledProcessError: If mmdc fails to render.
    """
    if shutil.which("mmdc") is None:
        raise FileNotFoundError(
            "mmdc not found. Install it with: npm install -g @mermaid-js/mermaid-cli"
        )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
        f.write(mermaid_code)
        tmp_path = f.name
    # npm install -g @mermaid-js/mermaid-cli
    # sudo apt-get update && sudo apt-get install -y libnss3 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libdrm2 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2t64 libxshmfence1
    # sudo apt-get install -y fonts-noto-cjk
    try:
        subprocess.run(
            ["mmdc", "-i", tmp_path, "-o", output_path, "-b", "transparent"],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return str(Path(output_path).resolve())


@env.task
def create_mindmap(topic: str, items: str, output_path: str):
    """Generate a mindmap PNG from topic and items.

    Args:
        topic: Root node text.
        items: JSON string of items list, e.g. '["A", "B", {"C": ["C1", "C2"]}]'
        output_path: Output PNG file path.
    """
    items_list = json.loads(items)
    mermaid_code = gen_mindmap_mermaid(topic, items_list)
    print(f"Generated Mermaid syntax:\n{mermaid_code}")
    result = mermaid_to_png(mermaid_code, output_path)
    print(f"PNG saved to: {result}")


create_mindmap(
    topic="Python學習",
    items='["基礎語法", "資料結構", {"Web框架": ["Flask", "Django", "FastAPI"]}, {"資料科學": ["Pandas", "NumPy"]}]',
    output_path="python_mindmap.png",
)
