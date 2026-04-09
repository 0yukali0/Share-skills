import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from create_mindmap import gen_mindmap_mermaid, mermaid_to_png


class TestGenMindmapMermaid:
    def test_basic_topic_with_items(self):
        result = gen_mindmap_mermaid("Python", ["Syntax", "Data Types", "Functions"])
        lines = result.strip().split("\n")
        assert lines[0] == "mindmap"
        assert lines[1].strip() == "Python"
        assert "Syntax" in result
        assert "Data Types" in result
        assert "Functions" in result

    def test_nested_structure(self):
        items = [
            {"Backend": ["Flask", "Django"]},
            {"Frontend": ["React", "Vue"]},
        ]
        result = gen_mindmap_mermaid("Web Dev", items)
        assert result.startswith("mindmap")
        assert "Web Dev" in result
        assert "Backend" in result
        assert "Flask" in result
        assert "Django" in result
        assert "Frontend" in result
        assert "React" in result
        assert "Vue" in result

    def test_empty_items(self):
        result = gen_mindmap_mermaid("Empty", [])
        lines = result.strip().split("\n")
        assert lines[0] == "mindmap"
        assert lines[1].strip() == "Empty"
        assert len(lines) == 2

    def test_mixed_items(self):
        items = ["Simple", {"Complex": ["Child1", "Child2"]}]
        result = gen_mindmap_mermaid("Root", items)
        assert "Simple" in result
        assert "Complex" in result
        assert "Child1" in result

    def test_deeply_nested(self):
        items = [{"L1": [{"L2": ["L3"]}]}]
        result = gen_mindmap_mermaid("Deep", items)
        assert "L1" in result
        assert "L2" in result
        assert "L3" in result

    def test_mermaid_syntax_valid_structure(self):
        result = gen_mindmap_mermaid("ML", ["Supervised", "Unsupervised"])
        lines = result.split("\n")
        # First line must be mindmap keyword
        assert lines[0] == "mindmap"
        # Each subsequent line should have indentation
        for line in lines[1:]:
            assert line.startswith("  ")


class TestMermaidToPng:
    def test_mmdc_not_installed(self):
        with patch("shutil.which", return_value=None):
            with pytest.raises(FileNotFoundError, match="mmdc not found"):
                mermaid_to_png("mindmap\n  root", "output.png")

    def test_successful_conversion(self, tmp_path):
        output_file = str(tmp_path / "test.png")
        mock_run = MagicMock(return_value=MagicMock(returncode=0))

        with patch("shutil.which", return_value="/usr/bin/mmdc"), \
             patch("subprocess.run", mock_run):
            result = mermaid_to_png("mindmap\n  root\n    A\n    B", output_file)

        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0][0] == "mmdc"
        assert "-i" in call_args[0][0]
        assert output_file in call_args[0][0]

    def test_mmdc_called_with_correct_args(self, tmp_path):
        output_file = str(tmp_path / "out.png")
        mock_run = MagicMock(return_value=MagicMock(returncode=0))

        with patch("shutil.which", return_value="/usr/bin/mmdc"), \
             patch("subprocess.run", mock_run):
            mermaid_to_png("mindmap\n  test", output_file)

        args = mock_run.call_args[0][0]
        assert args[0] == "mmdc"
        assert "-b" in args
        assert "transparent" in args

    @pytest.mark.skipif(
        shutil.which("mmdc") is None,
        reason="mmdc not installed"
    )
    def test_real_png_generation(self, tmp_path):
        output_file = str(tmp_path / "real_test.png")
        mermaid_code = gen_mindmap_mermaid("Test", ["A", "B", "C"])
        result = mermaid_to_png(mermaid_code, output_file)
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
