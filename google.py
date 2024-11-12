import argparse
import webbrowser
import pyperclip
from googlesearch import search
from tools.curses_wrapper import MenuSelector
import os

# Funktion zum Einlesen und Auflösen von Akronymen
test_file = "~/.acronymes.txt"
test_file = os.path.expanduser(test_file)


def resolve_acronym(ac: str) -> str:
    try:
        with open(test_file, "r") as file:
            for line in file:
                # Erwartet das Format "<akronym>:<url>"
                if ":" in line:
                    acronym, url = line.strip().split(":", 1)
                    if acronym == ac:
                        return url
    except FileNotFoundError:
        print(f"Die Datei '{test_file}' wurde nicht gefunden.")
    return None

# Funktion für die Menüauswahl, wenn kein Akronym angegeben wird


def select_acronym() -> str:
    acronyms = {}
    try:
        with open(test_file, "r") as file:
            for line in file:
                if ":" in line:
                    acronym, url = line.strip().split(":", 1)
                    acronyms[acronym] = {"url": url}
    except FileNotFoundError:
        print(f"Die Datei '{test_file}' wurde nicht gefunden.")
        return None

    # MenuSelector für die Auswahl eines Akronyms

    selector = MenuSelector(
        list(acronyms.keys()), prompt="Wählen Sie ein Akronym aus:")

    selected_option = selector.select()
    print(f"Ausgewählte Option: {selected_option}")

    return acronyms[selected_option]["url"] if selected_option else None

# Funktion für die Google-Suche


def google_search(query, result_num=1, key_string=None, open_url=True):
    if result_num == 0 and key_string is None:
        search_url = f"https://www.google.com/search?q={query}"
        if open_url:
            webbrowser.open(search_url)
            print(f"Öffne: {search_url}")
        else:
            pyperclip.copy(search_url)
            print(f"URL in den Copybuffer kopiert: {search_url}")
        return

    results = list(search(query, num_results=10))  # Top 10 Suchergebnisse

    if key_string:
        filtered_results = [url for url in results if key_string in url]
        if not filtered_results:
            print("Kein Ergebnis gefunden, das den Schlüsselbegriff enthält.")
            return
        result_url = filtered_results[0]
    else:
        if result_num > len(results) or result_num < 1:
            print("Ungültige Ergebnisnummer.")
            return
        result_url = results[result_num - 1]

    if open_url:
        webbrowser.open(result_url)
        print(f"Öffne: {result_url}")
    else:
        pyperclip.copy(result_url)
        print(f"URL in den Copybuffer kopiert: {result_url}")


def handle_acronym(acronym, url_only=False):
    acronym = acronym.strip()
    if acronym == "":
        # Wenn -a ohne Argument angegeben wurde, öffne den Curses-Selektor
        url = select_acronym().strip()
        if not url:
            print("Kein Akronym ausgewählt.")
        if url_only:
            pyperclip.copy(url)
        else:
            try:
                webbrowser.open(url)
                print(f"Öffne URL für das gewählte Akronym: {url}")
            except Exception as e:
                print(f"Fehler beim Öffnen der URL: {e}")
    else:
        # Direkte URL-Auflösung mit dem angegebenen Akronym
        url = resolve_acronym(acronym).strip()
        if url:
            webbrowser.open(url)
            print(f"Öffne URL für Akronym '{acronym}': {url}")
        else:
            print(f"Kein URL gefunden für das Akronym '{acronym}'.")
    return

# Hauptfunktion


def main():
    parser = argparse.ArgumentParser(
        description="Google-Such-Skript mit Akronymauflösung")

    # Definiere die Eingabeparameter
    parser.add_argument("search_term", nargs="?", default=None,
                        help="Der Suchbegriff für Google oder die Ergebnisnummer")
    parser.add_argument("result_num", nargs="?", default=0,
                        help="Die Ergebnisnummer oder der Schlüsselbegriff")
    parser.add_argument("-k", "--key", type=str,
                        help="Schlüsselbegriff für Filter in den Suchergebnissen")
    parser.add_argument("-u", "--url_only", action="store_true",
                        help="Kopiere nur die URL in den Zwischenspeicher")
    parser.add_argument("-a", "--acronym", type=str, nargs="?", const="",
                        help="Akronym für direkte URL-Auflösung")

    args = parser.parse_args()

    print(args)

    if args.acronym is not None:
        handle_acronym(args.acronym, args.url_only)
    else:
        # Falls `result_num` ein String ist, interpretiere ihn als `key_string`, außer `-k` wurde explizit angegeben
        if isinstance(args.result_num, str) and not args.result_num.isdigit() and args.key is None:
            args.key = args.result_num
            result_num = 1
        else:
            result_num = int(args.result_num)

        # Bestimme den Suchbegriff
        query = pyperclip.paste() if args.search_term is None else args.search_term

        # Führe die Suche durch
        google_search(query, result_num=result_num,
                      key_string=args.key, open_url=not args.url_only)


if __name__ == "__main__":
    main()
