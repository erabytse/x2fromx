import argparse
import sys
from .scanner import DirectoryScanner
from .builder import ProjectBuilder

def cmd_scan(args):
    try:
        scanner = DirectoryScanner(args.directory, args.output)
        _, count = scanner.save()
        print(f"✅ {count} éléments trouvés. Arborescence sauvegardée dans '{args.output}'.")
        if args.print_tree:
            with open(args.output, 'r', encoding='utf-8') as f:
                print("\n" + f.read())
    except Exception as e:
        print(f"❌ Erreur: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_build(args):
    try:
        builder = ProjectBuilder(args.structure_file, args.project_name)
        count, root = builder.build(overwrite=args.overwrite)
        print(f"✅ {count} éléments créés dans '{root}'.")
    except Exception as e:
        print(f"❌ Erreur: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog="x2fromx", description="Outils pour convertir des arborescences de projets en texte et vice-versa.")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    p_scan = subparsers.add_parser("scan", help="Scan un dossier et génère un fichier texte arborescent.")
    p_scan.add_argument("directory", help="Chemin vers le dossier à scanner.")
    p_scan.add_argument("-o", "--output", default="project_structure.txt", help="Fichier de sortie (défaut: project_structure.txt)")
    p_scan.add_argument("--print", dest="print_tree", action="store_true", help="Affiche l'arbre dans la console.")

    p_build = subparsers.add_parser("build", help="Crée une arborescence à partir d'un fichier texte.")
    p_build.add_argument("structure_file", help="Fichier texte contenant l'arborescence.")
    p_build.add_argument("-n", "--name", dest="project_name", default=None, help="Nom du dossier racine (défaut: new_project)")
    p_build.add_argument("--overwrite", action="store_true", help="Écrase le dossier s'il existe déjà.")

    args = parser.parse_args()
    if args.command == "scan": cmd_scan(args)
    elif args.command == "build": cmd_build(args)
    else: parser.print_help(); sys.exit(1)

if __name__ == "__main__":
    main()