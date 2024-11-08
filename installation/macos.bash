#!/bin/bash

# Dynamischen Pfad zu den Skripten und der requirements.txt ermitteln
SCRIPTSDIR=$(pwd)
echo "Script Directory: $SCRIPTSDIR"

REQUIREMENTS="$SCRIPTSDIR/requirements.txt"
TOOLS_DIR="/usr/local/bin"

echo Requirements: $REQUIREMENTS
echo Tools Directory: $TOOLS_DIR

# Sicherstellen, dass das Verzeichnis für die Tools existiert
mkdir -p "$TOOLS_DIR"

echo "=== Installing Python Environment ==="

# Erstelle eine Python-Umgebung im .tools-Ordner
cd "$TOOLS_DIR" || exit
sudo python3 -m venv .env

# Aktualisiere pip
sudo "$TOOLS_DIR/.env/bin/python" -m pip install --upgrade pip

# Installiere die Bibliotheken aus requirements.txt
sudo "$TOOLS_DIR/.env/bin/pip" install -r "$REQUIREMENTS"

echo "=== Creating Scripts ==="

# # Erstelle ein Skript für jedes Python-Skript im Skripte-Ordner
for script in "$SCRIPTSDIR"/*.py; do
    script_name=$(basename "$script" .py)
    echo "Creating script $script_name"

    # Erstelle das Bash-Skript für jedes Python-Skript
    touch "$SCRIPTSDIR/$script_name"
    echo "#!/usr/bin/env $TOOLS_DIR/.env/bin/python3" >> "$SCRIPTSDIR/$script_name"
    cat "$script" >> "$SCRIPTSDIR/$script_name"

    # Mach das Skript ausführbar
    chmod +x "$SCRIPTSDIR/$script_name"

    sudo mv "$SCRIPTSDIR/$script_name" "$TOOLS_DIR"
done

source ~/.bash_profile

echo "Setup abgeschlossen!"