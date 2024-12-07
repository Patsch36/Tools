import os
import re
import sys

# Unterstützte Dateiendungen mit zugehörigen Kommentar-Symbolen
LANGUAGE_COMMENT_SYMBOLS = {
    '.py': '#',
    '.rs': '//',
    '.java': '//',
    '.ts': '//',
    '.js': '//',
    '.c': '//',
    '.cpp': '//',
}

# Importmuster für unterstützte Sprachen
LANGUAGE_PATTERNS = {
    '.py': r'^import\s+(\w+)|from\s+(\w+)\s+import',
    '.rs': r'^use\s+([\w:]+);',
    '.java': r'^import\s+([\w.]+);',
    '.ts': r'^import\s+.*?from\s+[\'"]([\w/\.]+)[\'"];',
    '.js': r'^import\s+.*?from\s+[\'"]([\w/\.]+)[\'"];',
    '.c': r'^#include\s+[<"]([\w/\.]+)[">]',
    '.cpp': r'^#include\s+[<"]([\w/\.]+)[">]',
}


def find_imports(file_path, extension):
    """Extrahiere Imports/Includes basierend auf der Dateiendung."""
    pattern = LANGUAGE_PATTERNS.get(extension)
    if not pattern:
        return []

    imports = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                imports.append(match.group(1) or match.group(2))
    return imports


def find_file(import_name, extension, project_root):
    """Suche die Datei, die zu einem Import gehört."""
    for root, _, files in os.walk(project_root):
        for file in files:
            # Prüfe auf die richtige Dateiendung und den Importnamen
            if file.startswith(import_name) and file.endswith(extension):
                return os.path.join(root, file)
    return None


def merge_files(entry_file, project_root, output_file):
    """Kombiniere alle Dateien rekursiv in eine große Datei."""
    visited = set()  # Vermeide doppelte Verarbeitung
    stack = [entry_file]
    order = []  # Um die Reihenfolge umzukehren
    extension = os.path.splitext(entry_file)[1]
    comment_symbol = LANGUAGE_COMMENT_SYMBOLS.get(extension, '//')

    while stack:
        current_file = stack.pop()
        if current_file in visited:
            continue

        visited.add(current_file)
        order.append(current_file)

        # Analysiere die Imports und füge die entsprechenden Dateien dem Stack hinzu
        imports = find_imports(current_file, extension)
        for import_name in imports:
            imported_file = find_file(import_name, extension, project_root)
            if imported_file and imported_file not in visited:
                stack.append(imported_file)

    # Schreibe die Dateien in umgekehrter Reihenfolge
    with open(output_file, 'w', encoding='utf-8') as out:
        for file in reversed(order):
            with open(file, 'r', encoding='utf-8') as f:
                out.write(f"{comment_symbol} START OF {file}\n")
                for line in f:
                    if not re.match(LANGUAGE_PATTERNS.get(extension, ""), line):
                        out.write(line)
                out.write(f"{comment_symbol} END OF {file}\n\n")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python merge_files.py <entry_file> <project_root> <output_file>")
        sys.exit(1)

    entry_file = sys.argv[1]
    project_root = sys.argv[2]
    output_file = sys.argv[3]

    if not os.path.isfile(entry_file):
        print(f"Error: Entry file '{entry_file}' does not exist.")
        sys.exit(1)
    if not os.path.isdir(project_root):
        print(f"Error: Project root '{project_root}' is not a directory.")
        sys.exit(1)

    merge_files(entry_file, project_root, output_file)
    print(f"Merged files written to {output_file}")
