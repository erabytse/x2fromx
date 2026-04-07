import os
import re
import shutil
from pathlib import Path

class ProjectBuilder:
    def __init__(self, structure_file: str, root_name: str = None):
        self.structure_file = Path(structure_file)
        self.root_name = root_name
        if not self.structure_file.exists():
            raise FileNotFoundError(f"❌ Le fichier '{structure_file}' est introuvable.")

    def parse_structure(self) -> list[tuple[str, bool]]:
        paths = []
        with open(self.structure_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        path_stack = []
        for line in lines:
            raw_line = line.rstrip('\n')
            if not raw_line.strip(): continue
            clean_for_indent = re.sub(r'[│├└─]', ' ', raw_line)
            leading_spaces = len(clean_for_indent) - len(clean_for_indent.lstrip())
            depth = leading_spaces // 4
            cleaned = re.sub(r'.*?[├└][─]+\s*', '', raw_line)
            cleaned = re.sub(r'^[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0000FE00-\U0000FEFF]+', '', cleaned)
            cleaned = cleaned.split('#')[0].strip()
            if not cleaned: continue
            is_dir = cleaned.endswith('/')
            item_name = cleaned[:-1] if is_dir else cleaned
            while path_stack and path_stack[-1][0] >= depth:
                path_stack.pop()
            current_parts = [p[1] for p in path_stack] + [item_name]
            relative_path = os.path.join(*current_parts)
            paths.append((relative_path, is_dir))
            if is_dir:
                path_stack.append((depth, item_name))
        return paths

    def build(self, overwrite: bool = False) -> tuple[int, Path]:
        project_root = Path(self.root_name) if self.root_name else Path("new_project")
        if project_root.exists():
            if overwrite:
                shutil.rmtree(project_root)
            else:
                raise FileExistsError(f"⚠️ Le dossier '{project_root}' existe déjà. Ajoute `--overwrite` pour forcer.")
        project_root.mkdir(parents=True)
        created_count = 0
        paths = self.parse_structure()
        for rel_path, is_dir in paths:
            full_path = project_root / rel_path
            if is_dir:
                full_path.mkdir(parents=True, exist_ok=True)
                (full_path / ".gitkeep").touch(exist_ok=True)
                created_count += 1
            else:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                if not full_path.exists():
                    full_path.touch()
                    self._seed_content(full_path)
                    created_count += 1
        return created_count, project_root

    def _seed_content(self, file_path: Path):
        ext = file_path.suffix.lower()
        content = ""
        if ext == '.py': content = "# TODO: Implement logic\n\ndef main():\n    pass\n\nif __name__ == '__main__':\n    main()\n"
        elif ext == '.html': content = f"<!DOCTYPE html>\n<html>\n<head><title>{file_path.name}</title></head>\n<body></body>\n</html>"
        elif ext == '.md': content = f"# {file_path.stem}\n\nDocumentation to be written.\n"
        elif ext == '.js': content = f"// TODO: Implement JS logic for {file_path.name}\n"
        elif ext == '.css': content = f"/* Styles for {file_path.name} */\n"
        elif ext in ['.conf', '.sh', '.service']: content = f"# Configuration placeholder for {file_path.name}\n"
        if content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)