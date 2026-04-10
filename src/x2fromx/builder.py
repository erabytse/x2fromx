import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple, Dict, Optional

class ProjectBuilder:
    """Build a project directory structure from a text-based tree file."""
    
    def __init__(self, structure_file: str, root_name: str = None):
        self.structure_file = Path(structure_file).resolve()
        self.root_name = root_name
        
        if not self.structure_file.exists():
            raise FileNotFoundError(f"Error: Structure file '{structure_file}' not found.")

    def parse_structure(self) -> List[Tuple[str, bool]]:
        """Parse tree file and return list of (relative_path, is_dir) tuples."""
        paths = []
        path_stack = [] 

        with open(self.structure_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

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

    def build(self, overwrite: bool = False, verbose: bool = False, 
              credit: bool = False, seeds: Optional[Dict[str, str]] = None) -> Tuple[int, Path]:
        """Execute directory/file creation. Returns (created_count, root_path)."""
        project_root = Path(self.root_name) if self.root_name else Path("new_project")
        
        if project_root.exists():
            if overwrite:
                if verbose: print(f"🗑️  Removing existing: {project_root}")
                shutil.rmtree(project_root)
            else:
                raise FileExistsError(f"Error: Directory '{project_root}' already exists. Use --overwrite to force.")
        
        project_root.mkdir(parents=True)
        if verbose: print(f"🚀 Building project: {project_root.resolve()}")

        created_count = 0
        paths = self.parse_structure()
        seeds = seeds or {}
        
        for rel_path, is_dir in paths:
            full_path = project_root / rel_path
            
            if is_dir:
                full_path.mkdir(parents=True, exist_ok=True)
                (full_path / ".gitkeep").touch(exist_ok=True)
                created_count += 1
            else:
                if not is_dir:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    if not full_path.exists():
                        full_path.touch()
                        
                        # 🔧 Normalisation cross-platform pour la lookup des seeds
                        # Essayer avec les deux séparateurs au cas où
                        normalized_rel_path = rel_path.replace(os.sep, '/')

                        # 1. Check for injected seed content
                        content = seeds.get(normalized_rel_path)
                        
                        # 2. Fallback to default boilerplate
                        if content is None:
                            content = self._get_default_content(full_path)
                        
                        # 3. Append watermark if requested
                        if credit and content:
                            ext = full_path.suffix.lower()
                            if ext in ('.py', '.sh', '.conf', '.service', '.txt', '.md', '.yml', '.yaml', '.toml', '.ini'):
                                content += f"\n# Created with x2fromx | https://pypi.org/project/x2fromx/"
                            elif ext == '.js':
                                content += f"\n// Created with x2fromx | https://pypi.org/project/x2fromx/"
                            elif ext == '.css':
                                content += f"\n/* Created with x2fromx | https://pypi.org/project/x2fromx */"
                            else:
                                content += f"\n# Created with x2fromx | https://pypi.org/project/x2fromx/"
                                
                        if content:
                            full_path.write_text(content, encoding='utf-8')
                        created_count += 1
                    
        if verbose: print(f"✅ Created {created_count} items.")
        return created_count, project_root

    def _get_default_content(self, file_path: Path) -> str:
        """Return boilerplate content based on file extension."""
        ext = file_path.suffix.lower()
        if ext == '.py':
            return "# TODO: Implement logic\n\ndef main():\n    pass\n\nif __name__ == '__main__':\n    main()\n"
        elif ext == '.html':
            return f"<!DOCTYPE html>\n<html>\n<head><title>{file_path.name}</title></head>\n<body></body>\n</html>"
        elif ext == '.md':
            return f"# {file_path.stem}\n\nDocumentation to be written.\n"
        elif ext == '.js':
            return f"// TODO: Implement JS logic for {file_path.name}\n"
        elif ext == '.css':
            return f"/* Styles for {file_path.name} */\n"
        elif ext in ['.conf', '.sh', '.service']:
            return f"# Configuration placeholder for {file_path.name}\n"
        return ""