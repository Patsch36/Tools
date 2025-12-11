import os
import zipfile
import fnmatch
import argparse

def get_gitignore_patterns(gitignore_path):
    """Liest die .gitignore-Datei und gibt eine Liste von Mustern zurück."""
    if not os.path.exists(gitignore_path):
        return []
    
    patterns = []
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Kommentare und leere Zeilen ignorieren
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns

def is_ignored(path, ignore_patterns):
    """Prüft, ob ein Pfad (Datei oder Ordner) ignoriert werden soll."""
    for pattern in ignore_patterns:
        # Einfache Wildcard-Prüfung. Für eine vollständige gitignore-Syntax
        # (z.B. Negation '!') bräuchte man eine komplexere Logik.
        if fnmatch.fnmatch(path, pattern) or \
           any(fnmatch.fnmatch(part, pattern) for part in path.split(os.sep)):
            return True
    return False

def create_zip_from_project(source_dir, output_zip_file):
    """
    Erstellt ein ZIP-Archiv von einem Projektverzeichnis und ignoriert dabei
    Dateien und Ordner, die in .gitignore spezifiziert sind.
    """
    gitignore_path = os.path.join(source_dir, '.gitignore')
    ignore_patterns = get_gitignore_patterns(gitignore_path)
    
    # Füge Standard-Git- und Skript-Dateien zu den Ignoriermustern hinzu
    ignore_patterns.extend(['.git', '.git/*', os.path.basename(__file__), os.path.basename(output_zip_file)])

    print(f"Erstelle '{output_zip_file}' aus '{source_dir}'...")
    
    with zipfile.ZipFile(output_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Erstelle eine Kopie der Verzeichnisliste, um sie während der Iteration zu ändern
            # Dies ist wichtig, damit os.walk() die ignorierten Verzeichnisse nicht weiter durchläuft
            dirs[:] = [d for d in dirs if not is_ignored(os.path.relpath(os.path.join(root, d), source_dir), ignore_patterns)]
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_dir)
                
                if not is_ignored(relative_path, ignore_patterns):
                    print(f"  -> Füge hinzu: {relative_path}")
                    zipf.write(file_path, relative_path)
                else:
                    print(f"  -> Ignoriere: {relative_path}")

    print(f"\n✅ ZIP-Datei '{output_zip_file}' erfolgreich erstellt!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Packt ein Projektverzeichnis in eine ZIP-Datei und respektiert dabei die .gitignore-Regeln."
    )
    parser.add_argument("source_dir", nargs='?', default='.', 
                        help="Das Quellverzeichnis, das gezippt werden soll (Standard: aktuelles Verzeichnis).")
    parser.add_argument("-o", "--output", 
                        help="Name der Ausgabe-ZIP-Datei (Standard: <Verzeichnisname>.zip).")
    
    args = parser.parse_args()
    
    source_directory = args.source_dir
    
    if args.output:
        output_zip_name = args.output
    else:
        # Standard-Ausgabename aus dem Verzeichnisnamen ableiten
        dir_name = os.path.basename(os.path.abspath(source_directory))
        output_zip_name = f"{dir_name}.zip"

    create_zip_from_project(source_directory, output_zip_name)