# (macOS benötigt pyobjc, Windows Pillow + pyperclip und Linux xclip oder wl-copy.)

import sys
import os
import platform


def copy_image_macos(image_path):
    """Kopiert ein Bild in die macOS-Zwischenablage."""
    try:
        from AppKit import NSPasteboard, NSPasteboardTypePNG
        from Foundation import NSData

        image_path = os.path.abspath(image_path)
        image_data = NSData.dataWithContentsOfFile_(image_path)
        if image_data is None:
            print(f"❌ Fehler: Konnte Datei nicht lesen -> {image_path}")
            return

        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        pasteboard.setData_forType_(image_data, NSPasteboardTypePNG)
        print("✅ Bild wurde in die macOS-Zwischenablage kopiert!")
    except ImportError:
        print("❌ `pyobjc` nicht installiert. Installiere es mit `pip install pyobjc`.")


def copy_image_linux(image_path):
    """Kopiert ein Bild in die Linux-Zwischenablage mit `xclip` oder `wl-copy`."""
    if os.system("command -v xclip > /dev/null") == 0:
        os.system(f"xclip -selection clipboard -t image/png -i {image_path}")
        print("✅ Bild wurde mit `xclip` in die Zwischenablage kopiert!")
    elif os.system("command -v wl-copy > /dev/null") == 0:
        os.system(f"wl-copy < {image_path}")
        print("✅ Bild wurde mit `wl-copy` in die Zwischenablage kopiert!")
    else:
        print("❌ Weder `xclip` noch `wl-copy` gefunden! Installiere `xclip` oder `wl-clipboard`.")


def copy_image_windows(image_path):
    """Kopiert ein Bild in die Windows-Zwischenablage mit Pillow."""
    try:
        from PIL import Image
        import pyperclip

        image = Image.open(image_path)
        image.load()

        from io import BytesIO
        output = BytesIO()
        image.save(output, format="PNG")
        pyperclip.copy(output.getvalue())

        print("✅ Bild wurde in die Windows-Zwischenablage kopiert!")
    except ImportError:
        print("❌ `Pillow` oder `pyperclip` nicht installiert. Installiere sie mit:")
        print("   pip install pillow pyperclip")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️  Bitte gib den Pfad zum Bild an!")
        print("   Beispiel: python copy_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.isfile(image_path):
        print("❌ Fehler: Datei existiert nicht.")
        sys.exit(1)

    system_name = platform.system()
    if system_name == "Darwin":
        copy_image_macos(image_path)
    elif system_name == "Linux":
        copy_image_linux(image_path)
    elif system_name == "Windows":
        copy_image_windows(image_path)
    else:
        print(f"❌ Plattform {system_name} wird nicht unterstützt.")
