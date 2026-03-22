"""Convert a Markdown (.md) file to a LaTeX (.tex) file.

Usage:
    flyte run --local skill_impl/md_to_letex/md_to_letex.py md_to_letex --src doc.md --output doc.tex
"""

import flyte

env = flyte.TaskEnvironment(
    name="md_to_letex_env",
    image=flyte.Image.from_debian_base(python_version=(3, 13)).with_apt_packages(
        "texlive-xetex", "pandoc"
    ),
)


@env.task
def md_to_letex(src: str, output: str) -> None:
    import sys
    from pathlib import Path

    src_path = Path(src).resolve()

    if not src_path.exists():
        print(f"Error: source file not found: {src}", file=sys.stderr)
        sys.exit(1)

    md_text = src_path.read_text(encoding="utf-8")

    try:
        import pandoc

        doc = pandoc.read(md_text, format="markdown")
        pandoc.write(doc, format="latex", file=output, options=["--standalone"])
    except FileNotFoundError:
        print(
            "Error: pandoc binary not found.\n"
            "Install it with: sudo apt install pandoc  (or brew install pandoc on macOS)",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Saved: {output}")
