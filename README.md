# 🌲↔️📁 x2fromx

[![PyPI version](https://badge.fury.io/py/x2fromx.svg)](https://pypi.org/project/x2fromx/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Convert project directories ↔ text trees in one command.**  
> Built for developers & AI enthusiasts who need to scaffold projects from LLM outputs or extract codebase structure for context analysis.

---

## 🚀 Why `x2fromx`?
- 🤖 **AI-Ready**: Paste a `tree.txt` into ChatGPT/Claude, get a modified architecture back, and rebuild it instantly.
- ⚡ **Zero Dependencies**: Pure Python standard library. Works everywhere, instantly.
- 🧹 **Smart Filtering**: Automatically ignores `.git`, `node_modules`, `__pycache__`, binaries, and images.
- 🌱 **Auto-Seeding**: Creates boilerplate content (`.py`, `.html`, `.js`, etc.) so your IDE doesn't complain.
- 🖥️ **CLI & Library**: Use it in your terminal or import it directly into your Python scripts.

---

## 📦 Installation

```bash
pip install x2fromx
```

🛠️ CLI Usage
🔍 Scan a directory → generate a tree file

```bash
x2fromx scan ./my_existing_project -o structure.txt --print
```

🏗️ Build a project from a tree file
```
x2fromx build structure.txt -n my_new_project --overwrite
```

Available flags:

| Flag          | Description |
| :---          | :---           |
| scan <dir>    | Path to the folder to analyze |
| build <file>  | Path to the .txt tree file |
| -o, --output  | Output filename (default: project_structure.txt) |
| -n, --name    | Root project name for build (default: new_project) |
| --print       | Print the tree in the terminal after saving |
| --overwrite   | Force overwrite if the target folder already exists |


🤖 AI Workflow (The Killer Feature)

1. Extract context: x2fromx scan ./legacy_app -o context.txt
2. Ask an LLM: "Here is my project structure. Refactor it to add a /tests folder, split routes.py into a router package, and add a Dockerfile. Return the full tree."
3. Save the response: Paste the LLM's output into refactored.txt
4. Scaffold instantly: x2fromx build refactored.txt -n app_v2
5. Start coding: Your IDE opens a ready-to-use structure with placeholders.


🐍 Python API

```python
from x2fromx import DirectoryScanner, ProjectBuilder

# Scan
scanner = DirectoryScanner("./src", "tree.txt")
scanner.save()

# Build
builder = ProjectBuilder("tree.txt", "my_project")
count, root = builder.build(overwrite=True)
print(f"Created {count} items in {root}")

```

📁 Example Output
<!-- TREEVIEW START -->
```bash
my_project/
│
├── 📁 src/
│   ├── 📁 api/
│   │   ├── 📄 routes.py # Endpoint API
│   │   └── 📄 schemas.py
│   └── 📄 main.py # TODO: Implement logic
├── 📁 tests/
│   └── 📄 test_api.py # Tests unitaires
├── 📄 README.md # Documentation
└── 📄 requirements.txt # Dépendances Python
```
<!-- TREEVIEW END -->

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
1. Fork the repo
2. Create your feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request


📜 License

Distributed under the MIT License. See LICENSE for more information.

---

## 💙 Support 

If you use and value this tool, consider supporting its development:  
[![Sponsor](https://img.shields.io/badge/sponsor-erabytse-181717?logo=github)](https://github.com/sponsors/takouzlo)


[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web_Framework-green)](https://flask.palletsprojects.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)](https://typescriptlang.org)
[![AI](https://img.shields.io/badge/AI-ML-orange)](https://pytorch.org)
[![Founder](https://img.shields.io/badge/Founder-erabytse-purple)](https://github.com/erabytse)