import pyperclip
import argparse
from googletrans import Translator, LANGUAGES

def translate_clipboard(target_language):
    # Instanziiere den Übersetzer
    translator = Translator()

    # Text aus der Zwischenablage lesen
    text_to_translate = pyperclip.paste()
    if not text_to_translate:
        print("Die Zwischenablage ist leer.")
        return

    try:
        # Übersetze den Text
        translated_text = translator.translate(text_to_translate, dest=target_language)
        
        # Überprüfen, ob die Übersetzung erfolgreich war
        if translated_text is None:
            print("Die Übersetzung war nicht erfolgreich.")
            return
        
        # Übersetzten Text in die Zwischenablage kopieren
        pyperclip.copy(translated_text.text)
        print(f"Übersetzter Text wurde in die Zwischenablage.")

    except Exception as e:
        print(f"Fehler bei der Übersetzung: {e}")

if __name__ == "__main__":
    # ArgumentParser erstellen
    parser = argparse.ArgumentParser(description="Übersetze den Text aus der Zwischenablage in die angegebene Sprache.")
    parser.add_argument("language", type=str, help="Die Sprache, in die der Text übersetzt werden soll (ISO-Code).")

    # Argumente parsen
    args = parser.parse_args()

    # Überprüfen, ob die angegebene Sprache gültig ist
    if args.language not in LANGUAGES:
        print("Ungültiger ISO-Code für die Sprache. Verfügbare Sprachen sind:")
        print(", ".join([f"{lang} ({code})" for code, lang in LANGUAGES.items()]))
    else:
        # Übersetzen und in die Zwischenablage kopieren
        translate_clipboard(args.language)
