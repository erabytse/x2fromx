import os
import sys
from pathlib import Path

class DirectoryScanner:
    def __init__(self, root_path: str, output_file: str = "project_structure.txt"):
        self.root_path = Path(root_path).resolve()
        self.output_file = output_file
        self.ignore_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'env', '.idea', '.vscode', 'build', 'dist', '.pytest_cache',
            'migrations', 'static_collected'
        }
        self.ignore_extensions = {
            '.pyc', '.pyo', '.so', '.dll', '.exe', '.log', '.db', '.sqlite',
            '.jpg', '.jpeg', '.png', '.gif', '.ico', '.woff', '.woff2', '.ttf',
            '.DS_Store', '.env'
        }

    def scan(self) -> list:
        structure = []
        if not self.root_path.exists():
            raise FileNotFoundError(f"❌ Le dossier '{self.root_path}' n'existe pas.")

        for dirpath, dirnames, filenames in os.walk(self.root_path):
            dirnames[:] = [d for d in dirnames if d not in self.ignore_dirs and not d.startswith('.')]
            dirnames.sort()
            current_path = Path(dirpath)
            relative_depth = len(current_path.relative_to(self.root_path).parts)
            
            if current_path != self.root_path:
                structure.append({'type': 'dir', 'name': current_path.name, 'depth': relative_depth, 'path': current_path})
                
            valid_files = [f for f in filenames if not f.startswith('.') and Path(f).suffix.lower() not in self.ignore_extensions]
            valid_files.sort()
            for filename in valid_files:
                file_path = current_path / filename
                structure.append({'type': 'file', 'name': filename, 'depth': relative_depth + 1, 'path': file_path, 'ext': Path(filename).suffix.lower()})
        return structure

    def generate_tree_text(self, structure: list) -> str:
        if not structure: return ""
        lines = [f"{self.root_path.name}/", "│"]
        is_last_map = {}
        for i, item in enumerate(structure):
            next_item = structure[i+1] if i+1 < len(structure) else None
            is_last_map[i] = next_item['depth'] <= item['depth'] if next_item else True

        for i, item in enumerate(structure):
            depth, is_last = item['depth'], is_last_map[i]
            is_dir = item['type'] == 'dir'
            prefix = ""
            for d in range(1, depth):
                parent_is_last = self._check_parent_status(structure, i, d)
                prefix += "     " if parent_is_last else "│    "
            branch = "└── " if is_last else "├── "
            icon = "📁 " if is_dir else "📄 "
            name = f"{item['name']}/" if is_dir else item['name']
            comment = ""
            if not is_dir:
                ext = item.get('ext', '')
                if name == "requirements.txt": comment = " # Dépendances Python"
                elif name == "wsgi.py": comment = " # Point d'entrée Apache"
                elif name == "manager.py": comment = " # Cœur logique"
                elif name == "routes.py": comment = " # Routes Web"
                elif ext == ".md": comment = " # Documentation"
                elif ext == ".html": comment = " # Template UI"
                elif ext == ".js": comment = " # Logique Frontend"
                elif ext == ".css": comment = " # Styles"
                elif ext == ".py":
                    if "test" in item['path'].parts: comment = " # Tests unitaires"
                    elif "api" in item['path'].parts: comment = " # Endpoint API"
            lines.append(f"{prefix}{branch}{icon}{name}{comment}")
        return "\n".join(lines)

    def _check_parent_status(self, structure, current_index, target_depth):
        for i in range(current_index - 1, -1, -1):
            if structure[i]['depth'] == target_depth:
                next_item = structure[i+1] if i+1 < len(structure) else None
                return next_item['depth'] <= target_depth if next_item else True
        return False

    def save(self) -> tuple[str, int]:
        structure = self.scan()
        tree_content = self.generate_tree_text(structure)
        full_content = f"# Structure générée automatiquement pour {self.root_path.name}\n# Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{tree_content}\n"
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
        return full_content, len(structure)