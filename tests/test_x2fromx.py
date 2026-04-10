import os
import subprocess
import sys
import pytest
from pathlib import Path
from x2fromx import __version__, DirectoryScanner, ProjectBuilder

# Force UTF-8 pour les subprocess (critique sous Windows)
ENV_UTF8 = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}

def test_version():
    assert __version__ == "0.1.3"

def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "x2fromx.cli", "--help"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env=ENV_UTF8
    )
    assert result.returncode == 0, f"CLI failed with: {result.stderr}"
    assert "scan" in result.stdout and "build" in result.stdout

def test_build_with_seed_and_credit(tmp_path):
    # 1. Arbre minimal et propre
    tree_file = tmp_path / "tree.txt"
    tree_content = "project_root/\n    └── config.py"
    tree_file.write_text(tree_content, encoding='utf-8')

    # 2. Init builder
    out_dir = tmp_path / "output"
    builder = ProjectBuilder(str(tree_file), str(out_dir))
    
    # 3. Injection : utiliser pathlib pour la clé (cross-platform)
    seed_key = str(Path("project_root") / "config.py")
    seeds = {seed_key: "# My custom config\nprint('seed_ok')"}
    
    builder.build(credit=True, seeds=seeds)

    # 4. Vérification du chemin réel créé
    config_path = out_dir / "project_root" / "config.py"
    assert config_path.exists(), f"File not created at {config_path}"

    content = config_path.read_text(encoding='utf-8')
    assert "# My custom config" in content, f"❌ Seed missing. Got:\n{content}"
    assert "Created with x2fromx" in content, "❌ Watermark missing"