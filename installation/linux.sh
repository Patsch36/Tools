#!/bin/bash

# Dynamischen Pfad zu den Skripten und der requirements.txt ermitteln
SCRIPTSDIR=$(pwd)
REQUIREMENTS="$SCRIPTSDIR/requirements.txt"
TOOLS_DIR="$HOME/.tools"
mkdir -p $TOOLS_DIR

# Funktion zum Installieren von xclip oder xsel basierend auf dem Paketmanager
install_clipboard_tool() {
    # Überprüfen, ob apt (Debian/Ubuntu-basierte Distributionen) vorhanden ist
    if command -v apt-get &> /dev/null; then
        echo "Debian/Ubuntu-basierte Distribution erkannt. Installiere xclip oder xsel..."
        sudo apt-get update
        # Versuche zuerst xsel zu installieren, falls es fehlschlägt, dann xclip installieren
        if ! dpkg -l | grep -q xsel; then
            sudo apt-get install -y xsel && sudo apt-get install -y xclip
        else
            echo "xsel ist bereits installiert."
        fi

    # Überprüfen, ob dnf (Fedora/RHEL/CentOS-basierte Distributionen) vorhanden ist
    elif command -v dnf &> /dev/null; then
        echo "Fedora/CentOS-basierte Distribution erkannt. Installiere xclip oder xsel..."
        sudo dnf install -y xsel && sudo dnf install -y xclip

    # Überprüfen, ob pacman (Arch Linux-basierte Distributionen) vorhanden ist
    elif command -v pacman &> /dev/null; then
        echo "Arch Linux-basierte Distribution erkannt. Installiere xclip oder xsel..."
        sudo pacman -S --noconfirm xsel && sudo pacman -S --noconfirm xclip

    else
        echo "Nicht unterstützte Distribution. Bitte installiere manuell entweder xclip oder xsel."
        exit 1
    fi
}

# Erstelle eine Python Umgebung im .tools Ordner
cd $TOOLS_DIR
python3 -m venv .env
$TOOLS_DIR/.env/bin/python -m pip install --upgrade pip

# Installiere die Bibliotheken aus requirements.txt
$TOOLS_DIR/.env/bin/pip install -r $REQUIREMENTS

# Überprüfen, ob xclip oder xsel bereits installiert ist
if ! command -v xclip &> /dev/null && ! command -v xsel &> /dev/null; then
    echo "Kein Clipboard-Tool gefunden. Installiere eines..."
    install_clipboard_tool
else
    echo "Clipboard-Tool (xclip oder xsel) ist bereits installiert."
fi

# Erstelle ein Skript für jedes Python-Skript im Skripte-Ordner
for script in $SCRIPTSDIR/*.py; do
    script_name=$(basename "$script" .py)
    echo "#!/bin/bash" > "$TOOLS_DIR/$script_name"
    echo "$TOOLS_DIR/.env/bin/python $script \$@" >> "$TOOLS_DIR/$script_name"
    chmod +x "$TOOLS_DIR/$script_name"
done

# Fügt das .tools Verzeichnis zur PATH-Umgebungsvariable hinzu
echo "export PATH=\$PATH:$TOOLS_DIR" >> ~/.bashrc
source ~/.bashrc

# Frage, ob das Skript auf einem Server installiert wird
read -p "Wird dieses Setup auf einem Server (ohne GUI) installiert? (j/n; j:Display Variable wird gesetzt): " is_server
if [[ "$is_server" =~ ^[JjYy]$ ]]; then
    if ! grep -q "^export DISPLAY=:0" ~/.bashrc; then
        echo "export DISPLAY=:0" >> ~/.bashrc
        export DISPLAY=:0
    fi
fi

echo "Setup abgeschlossen!"