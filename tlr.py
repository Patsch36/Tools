import pyperclip
import argparse
from googletrans import Translator, LANGUAGES


def translate_text(target_language, text=None, to_clipboard=True, print_output=True):
    # Instantiate the translator
    translator = Translator()

    # Read text from clipboard if no text is provided
    if text is None:
        text = pyperclip.paste()
        if not text:
            if print_output:
                print("The clipboard is empty.")
            return
        if print_output:
            print(f"Translating the following text to '{
                  LANGUAGES[target_language]}': {text}")
    else:
        if print_output:
            print(f"Translating to '{LANGUAGES[target_language]}'")

    try:
        # Translate the text
        translated_text = translator.translate(text, dest=target_language)

        # Check if the translation was successful
        if translated_text is None:
            if print_output:
                print("The translation was not successful.")
            return

        # Copy translated text to clipboard
        if to_clipboard:
            pyperclip.copy(translated_text.text)
            if print_output:
                print("Translated text has been copied to the clipboard.")

    except Exception as e:
        if print_output:
            print(f"Error during translation: {e}")
        else:
            raise e

    return translated_text.text


if __name__ == "__main__":
    # Create ArgumentParser
    parser = argparse.ArgumentParser(
        description="Translate text from the clipboard or the provided text to the specified language.")
    parser.add_argument(
        "text", type=str, nargs='?', help="The text to be translated.", default=None)
    parser.add_argument(
        "-l", "--language", type=str, help="The language to translate the text to (ISO code).", required=False, default="en")

    # Parse arguments
    args = parser.parse_args()

    # Check if the specified language is valid
    if args.language not in LANGUAGES:
        print("Invalid ISO code for the language. Available languages are:")
        print(
            ", ".join([f"{lang} ({code})" for code, lang in LANGUAGES.items()]))
    else:
        # Translate and copy to clipboard
        translate_text(args.language, args.text)
