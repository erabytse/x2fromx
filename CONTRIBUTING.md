# Contributing to x2fromx

Thank you for your interest in contributing to `x2fromx`! 🌲✨  
This project aims to simplify project scaffolding and codebase analysis for developers and AI workflows. Every contribution—code, docs, or bug reports—is highly appreciated.

## 🛠️ Getting Started

1. **Fork & Clone**
   ```bash
   git clone https://github.com/erabytse/x2fromx.git
   cd x2fromx
   ```

2. Create a Virtual Environment
    ```bash
    python -m venv .your_venv
    source .your_venv/bin/activate  # Windows: .your_venv\Scripts\activate
    ```

3. Install in Editable Mode
    ```bash
    pip install -e .
    pip install pytest
    ```

4. Run Tests
    ```bash
    pytest tests/
    ```

    📝 How to Contribute

    🐛 Reporting Issues

    - Use the GitHub Issue Tracker
    - Include: Python version, OS, steps to reproduce, expected vs actual behavior
    - For parsing/rendering bugs, attach a sample tree.txt or target directory


    💻 Submitting Code

    1. Create a feature branch: git checkout -b feat/your-feature
    2. Write clean, readable code. Keep it compatible with Python 3.8+
    3. Add/update tests in tests/
    4. Commit using Conventional Commits:
    ```bash
    git commit -m "feat: add custom ignore patterns"
    git commit -m "fix: parser crash on empty lines"
    git commit -m "docs: update README examples"
    ```

5. Push and open a Pull Request

    🧪 Testing Guidelines

    - Use pytest with tmp_path or pathlib for filesystem mocking
    - Test both CLI behavior and core classes (DirectoryScanner, ProjectBuilder)
    - Cover edge cases: nested dirs, special characters, missing files, large trees, mixed encodings
    - Keep tests fast and deterministic

    📐 Code Style

    - Follow PEP 8
    - Use type hints where possible
    - Keep functions focused; prefer composition over inheritance
    - No external dependencies unless strictly necessary (core philosophy: stdlib-only CLI)

    📄 Pull Request Checklist

    - Tests pass locally (pytest)
    - Code follows PEP 8 & project conventions
    - Documentation/README updated if CLI behavior changed
    - Commit messages are clear and conventional
    - PR description explains the "why" and "what"

    🤝 Community Guidelines

    - Be respectful and constructive
    - Help review others' PRs
    - Ask questions in Issues/Discussions before starting major changes


📜 License
    By contributing, you agree that your contributions will be licensed under the MIT License.


💡 Need help? Open an issue with the question label or start a Discussion. We're here to help you get started!