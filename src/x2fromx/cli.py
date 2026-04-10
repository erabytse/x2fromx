#!/usr/bin/env python3
"""Command-line interface for x2fromx."""
import sys

# 🔧 Force UTF-8 pour les terminaux Windows (évite les crashs charmap)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
    
import argparse
from importlib.metadata import version, PackageNotFoundError

from .scanner import DirectoryScanner
from .builder import ProjectBuilder


def get_version() -> str:
    try: return version("x2fromx")
    except PackageNotFoundError: return "0.1.2-dev"

def parse_seeds(seed_args):
    """Parse --seed 'path|content' arguments into a dict."""
    seeds = {}
    if not seed_args: return seeds
    for s in seed_args:
        if '|' in s:
            path, content = s.split('|', 1)
            seeds[path.strip()] = content
    return seeds

def cmd_scan(args):
    try:
        scanner = DirectoryScanner(args.directory, args.output)
        _, count = scanner.save(verbose=args.verbose)
        if not args.verbose: print(f"✅ Scanned {count} items. Tree saved to '{args.output}'.")
        if args.print_tree:
            with open(args.output, 'r', encoding='utf-8') as f: print("\n" + f.read())
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr); sys.exit(1)

def cmd_build(args):
    try:
        seeds = parse_seeds(args.seed)
        builder = ProjectBuilder(args.structure_file, args.project_name)
        count, root = builder.build(
            overwrite=args.overwrite, 
            verbose=args.verbose, 
            credit=args.credit, 
            seeds=seeds
        )
        if not args.verbose: print(f"✅ Created {count} items in '{root}'.")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr); sys.exit(1)

def cmd_credits(args):
    from ._ascii import ERABYTSE_ASCII, TAGLINE
    print(ERABYTSE_ASCII)
    print(f"\n✨ {TAGLINE}\n")

def main():
    parser = argparse.ArgumentParser(
        prog="x2fromx",
        description="Convert project directories ↔ text trees. Ideal for AI scaffolding & codebase analysis.",
        epilog="Examples:\n  x2fromx scan ./my_project -o tree.txt\n  x2fromx build tree.txt -n app --seed 'README.md|My App\n--credit",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {get_version()}')
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Scan
    p_scan = subparsers.add_parser("scan", help="Scan a directory and generate a tree file")
    p_scan.add_argument("directory", help="Path to directory to scan")
    p_scan.add_argument("-o", "--output", default="project_structure.txt", help="Output file (default: project_structure.txt)")
    p_scan.add_argument("--print", dest="print_tree", action="store_true", help="Print tree to console after saving")
    p_scan.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    p_scan.set_defaults(func=cmd_scan)

    # Build
    p_build = subparsers.add_parser("build", help="Create a project from a tree file")
    p_build.add_argument("structure_file", help="Path to tree file")
    p_build.add_argument("-n", "--name", dest="project_name", default=None, help="Project root name (default: new_project)")
    p_build.add_argument("--overwrite", action="store_true", help="Overwrite if project directory exists")
    p_build.add_argument("--credit", action="store_true", help="Add x2fromx watermark to generated files")
    p_build.add_argument("--seed", nargs="+", help="Inject content: --seed 'path/to/file.txt|Custom content'")
    p_build.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    p_build.set_defaults(func=cmd_build)

    # Credits
    p_credits = subparsers.add_parser("credits", help="Show Erabytse ASCII art & project info")
    p_credits.set_defaults(func=cmd_credits)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()