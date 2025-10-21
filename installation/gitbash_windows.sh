#!/bin/bash

# Dynamischen Pfad zu den Skripten und der requirements.txt ermitteln
SCRIPTSDIR=$(dirname "$(dirname "$(realpath "$0")")")
echo "Script Directory: $SCRIPTSDIR"

REQUIREMENTS="$SCRIPTSDIR/requirements.txt"
echo "Requirements File: $REQUIREMENTS"

TOOLS_DIR="$HOME/.tools"
echo "Tools Directory: $TOOLS_DIR"

# Erstelle das .tools Verzeichnis im Benutzerverzeichnis
mkdir -p "$TOOLS_DIR"

echo "=== Installing Python Environment ==="

# Erstelle eine Python Umgebung im .tools Ordner
cd "$TOOLS_DIR"
python -m venv .env

# Aktualisiere pip
"$TOOLS_DIR/.env/Scripts/python.exe" -m pip install --upgrade pip

# Installiere die Bibliotheken aus requirements.txt
"$TOOLS_DIR/.env/Scripts/python.exe" -m pip install -r "$REQUIREMENTS"

# Installiere windows-curses für Git Bash/Windows
"$TOOLS_DIR/.env/Scripts/python.exe" -m pip install windows-curses

# Installiere pillow + pyperclip
"$TOOLS_DIR/.env/Scripts/python.exe" -m pip install pillow pyperclip

echo "=== Creating Custom Scripts ==="

# Erstelle die Skripte für jedes Python-Skript im Skripte-Ordner
for script in "$SCRIPTSDIR"/*.py; do
    if [[ -f "$script" ]]; then
        script_name=$(basename "$script" .py)
        echo "Creating Tool $script_name"
        
        # Erstelle ein Bash-Skript für Git Bash
        cat > "$TOOLS_DIR/$script_name" << EOF
#!/bin/bash
export PYTHONPATH="$SCRIPTSDIR"
"$TOOLS_DIR/.env/Scripts/python.exe" "$script" "\$@"
EOF
        
        # Mache das Skript ausführbar
        chmod +x "$TOOLS_DIR/$script_name"
        
        # Erstelle auch eine .bat Datei für bessere Windows-Kompatibilität
        cat > "$TOOLS_DIR/$script_name.bat" << EOF
@echo off
set PYTHONPATH=$SCRIPTSDIR
"$TOOLS_DIR\.env\Scripts\python.exe" "$script" %*
EOF
    fi
done

echo "=== Adding .tools to PATH ==="

# Füge das .tools Verzeichnis zur PATH-Umgebungsvariable hinzu
# Überprüfe, ob der Pfad bereits in der .bashrc vorhanden ist
if ! grep -q "export PATH.*$TOOLS_DIR" ~/.bashrc 2>/dev/null; then
    echo "export PATH=\"\$PATH:$TOOLS_DIR\"" >> ~/.bashrc
    echo "PATH updated in ~/.bashrc"
else
    echo "PATH already contains $TOOLS_DIR"
fi

# Überprüfe, ob der Pfad bereits in der .bash_profile vorhanden ist (für Git Bash)
if ! grep -q "export PATH.*$TOOLS_DIR" ~/.bash_profile 2>/dev/null; then
    echo "export PATH=\"\$PATH:$TOOLS_DIR\"" >> ~/.bash_profile
    echo "PATH updated in ~/.bash_profile"
else
    echo "PATH already contains $TOOLS_DIR in .bash_profile"
fi

# Aktualisiere die aktuelle Session
export PATH="$PATH:$TOOLS_DIR"

# Setze auch die Windows PATH über setx (für bessere Integration)
echo "=== Updating Windows PATH ==="
if command -v setx.exe &> /dev/null; then
    # Konvertiere Unix-Pfad zu Windows-Pfad
    TOOLS_DIR_WIN=$(cygpath -w "$TOOLS_DIR" 2>/dev/null || echo "$TOOLS_DIR" | sed 's|^/c/|C:/|' | sed 's|/|\\|g')
    setx.exe PATH "$TOOLS_DIR_WIN;%PATH%" 2>/dev/null || echo "Warning: Could not update Windows PATH automatically"
    echo "Windows PATH updated via setx"
else
    echo "Note: setx not available. Please manually add $TOOLS_DIR to your Windows PATH"
fi

echo ""
echo "=== Setup Complete! ==="
echo "Please restart your Git Bash terminal or run 'source ~/.bashrc' to use the new tools."
echo "Available tools can be found in: $TOOLS_DIR"