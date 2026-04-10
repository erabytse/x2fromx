import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class DirectoryScanner:
    """Scan a directory and generate a text-based tree structure."""
    
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

    def scan(self) -> List[Dict]:
        """Return a structured list of valid files/directories."""
        structure = []
        
        if not self.root_path.exists():
            raise FileNotFoundError(f"Error: Directory '{self.root_path}' not found.")

        for dirpath, dirnames, filenames in os.walk(self.root_path):
            dirnames[:] = [d for d in dirnames if d not in self.ignore_dirs and not d.startswith('.')]
            dirnames.sort()
            
            current_path = Path(dirpath)
            relative_depth = len(current_path.relative_to(self.root_path).parts)
            
            if current_path != self.root_path:
                structure.append({
                    'type': 'dir',
                    'name': current_path.name,
                    'depth': relative_depth,
                    'path': current_path
                })

            valid_files = [f for f in filenames 
                          if not f.startswith('.') and Path(f).suffix.lower() not in self.ignore_extensions]
            valid_files.sort()
            
            for filename in valid_files:
                file_path = current_path / filename
                structure.append({
                    'type': 'file',
                    'name': filename,
                    'depth': relative_depth + 1,
                    'path': file_path,
                    'ext': Path(filename).suffix.lower()
                })
        return structure

    def generate_tree_text(self, structure: List[Dict]) -> str:
        """Convert structured list to ASCII tree format."""
        if not structure:
            return ""

        lines = [f"{self.root_path.name}/", "│"]
        is_last_map = {}
        
        for i, item in enumerate(structure):
            depth = item['depth']
            next_item = structure[i+1] if i+1 < len(structure) else None
            is_last_map[i] = next_item['depth'] <= depth if next_item else True

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
                if name == "requirements.txt": comment = " # Python dependencies"
                elif name == "wsgi.py": comment = " # Apache entry point"
                elif name == "manager.py": comment = " # Core logic"
                elif name == "routes.py": comment = " # Web routes"
                elif ext == ".md": comment = " # Documentation"
                elif ext == ".html": comment = " # UI template"
                elif ext == ".js": comment = " # Frontend logic"
                elif ext == ".css": comment = " # Styles"
                elif ext == ".py":
                    if "test" in item['path'].parts: comment = " # Unit tests"
                    elif "api" in item['path'].parts: comment = " # API endpoint"
                    
            lines.append(f"{prefix}{branch}{icon}{name}{comment}")
            
        return "\n".join(lines)

    def _check_parent_status(self, structure: List[Dict], current_index: int, target_depth: int) -> bool:
        """Check if parent at target_depth is the last sibling."""
        for i in range(current_index - 1, -1, -1):
            if structure[i]['depth'] == target_depth:
                next_item = structure[i+1] if i+1 < len(structure) else None
                return next_item['depth'] <= target_depth if next_item else True
        return False

    def save(self, verbose: bool = False) -> Tuple[str, int]:
        """Scan and save tree to file. Returns (content, item_count)."""
        if verbose:
            print(f"🔍 Scanning: {self.root_path}")
            
        structure = self.scan()
        tree_content = self.generate_tree_text(structure)
        full_content = (f"# Auto-generated structure for {self.root_path.name}\n"
                       f"# Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                       f"{tree_content}\n")
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        if verbose:
            print(f"📦 Found {len(structure)} items (after filtering).")
            print(f"✅ Saved to '{self.output_file}'.")
            
        return full_content, len(structure)