"""Compile a LaTeX (.tex) file to PDF.

Usage:
    flyte run --local skill_impl/letex_to_pdf/letex_to_pdf.py letex_to_pdf --src doc.tex --output doc.pdf
"""

import flyte

env = flyte.TaskEnvironment(
    name="letex_to_pdf_env",
    image=flyte.Image.from_debian_base(
        name="letex_to_pdf_env", python_version=(3, 13)
    ).with_apt_packages("texlive-xetex"),
)


@env.task
def letex_to_pdf(src: str, output: str) -> str:
    import shutil
    import subprocess
    import sys
    import tempfile
    from pathlib import Path

    src_path = Path(src).resolve()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_tex = Path(tmpdir) / src_path.name
        shutil.copy2(src_path, tmp_tex)

        # Run xelatex twice for cross-references / TOC (supports UTF-8 and CJK)
        for _ in range(2):
            result = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", tmp_tex.name],
                cwd=tmpdir,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )

        tmp_pdf = Path(tmpdir) / src_path.with_suffix(".pdf").name

        if tmp_pdf.exists():
            if result.returncode != 0:
                print(
                    f"Warning: pdflatex exited with code {result.returncode} but produced a PDF.\n"
                    f"{result.stdout[-2000:]}",
                    file=sys.stderr,
                )
            shutil.copy2(tmp_pdf, output)
        else:
            print(
                f"Warning: xelatex failed (exit {result.returncode}), generating blank PDF.\n"
                f"{result.stdout[-2000:]}",
                file=sys.stderr,
            )
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.output(output)
            return output

    print(f"Saved: {output}")
    return output
