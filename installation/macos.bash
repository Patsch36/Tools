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
sudo python3 -m venv .tools_env

# Aktualisiere pip
sudo "$TOOLS_DIR/.tools_env/bin/python" -m pip install --upgrade pip

# Installiere die Bibliotheken aus requirements.txt
sudo "$TOOLS_DIR/.tools_env/bin/pip" install -r "$REQUIREMENTS"

sudo "$TOOLS_DIR/.tools_env/bin/pip" install pyobjc

echo "=== Creating Scripts ==="

# Erstelle ein Skript für jedes Python-Skript im Skripte-Ordner
for script in "$SCRIPTSDIR"/*.py; do
    script_name=$(basename "$script" .py)
    echo "Creating script $script_name"

    # Extrahiere den Inhalt des Skripts
    script_content=$(cat "$script")

    # Überprüfen, ob ein Import aus 'tools' vorhanden ist
    if echo "$script_content" | grep -q "from tools\."; then
        # Finde alle Imports aus dem tools-Verzeichnis mit awk (anstatt grep -P)
        imports=$(echo "$script_content" | awk -F'tools.' '{for(i=2;i<=NF;i++) print $i}' | awk -F' ' '{print $1}')

        # Füge den Inhalt der importierten Dateien am Anfang hinzu und entferne den Import
        for import in $imports; do
            # Extrahiere den Inhalt der importierten Datei aus dem tools-Verzeichnis
            tool_script="$SCRIPTSDIR/tools/$import.py"
            if [[ -f "$tool_script" ]]; then
                echo "Adding content of $tool_script"
                tool_content=$(cat "$tool_script")
                script_content="$tool_content"$'\n'"$script_content"

                # Entferne den Import aus der Skriptdatei
                script_content=$(echo "$script_content" | sed '/from tools\.'"$import"'/d')
            else
                echo "Warning: $tool_script not found"
            fi
        done
    fi

    # Erstelle das Bash-Skript für jedes Python-Skript
    echo "#!/usr/bin/env $TOOLS_DIR/.tools_env/bin/python3" > "$SCRIPTSDIR/$script_name"
    echo "$script_content" >> "$SCRIPTSDIR/$script_name"

    # Mach das Skript ausführbar
    chmod +x "$SCRIPTSDIR/$script_name"

    # Verschiebe das Skript ins Tools-Verzeichnis
    sudo mv "$SCRIPTSDIR/$script_name" "$TOOLS_DIR"
done

source ~/.bash_profile

echo "Setup abgeschlossen!"
