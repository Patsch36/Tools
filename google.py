import argparse
import webbrowser
import pyperclip
from googlesearch import search


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
        # Suche nach dem ersten Treffer, der den `key_string` enthält
        filtered_results = [url for url in results if key_string in url]
        if not filtered_results:
            print("Kein Ergebnis gefunden, das den Schlüsselbegriff enthält.")
            return
        result_url = filtered_results[0]
    else:
        # Hole das spezifische Ergebnis basierend auf der Ergebnisnummer
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


def main():
    parser = argparse.ArgumentParser(description="Google-Such-Skript")

    # Definiere mögliche Eingabeparameter
    parser.add_argument("search_term", nargs="?", default=None,
                        help="Der Suchbegriff für Google oder die Ergebnisnummer")
    parser.add_argument("result_num", nargs="?", default=0,
                        help="Die Ergebnisnummer oder der Schlüsselbegriff")
    parser.add_argument("-k", "--key", type=str,
                        help="Schlüsselbegriff für Filter in den Suchergebnissen")
    parser.add_argument("-u", "--url_only", action="store_true",
                        help="Kopiere nur die URL in den Zwischenspeicher")

    args = parser.parse_args()

    # Falls `result_num` ein String ist, interpretiere ihn als `key_string`, außer `-k` wurde explizit angegeben
    if isinstance(args.result_num, str) and not args.result_num.isdigit() and args.key is None:
        args.key = args.result_num  # Nutze `result_num` als `key_string`
        result_num = 1  # Setze `result_num` auf 1 (erstes Ergebnis)
    else:
        result_num = int(args.result_num)

    # Bestimme den Suchbegriff
    if args.search_term is None:
        # Kein Suchbegriff gegeben, benutze den Copybuffer als Suchbegriff
        query = pyperclip.paste()
    else:
        query = args.search_term

    # Führe die Suche durch
    google_search(query, result_num=result_num,
                  key_string=args.key, open_url=not args.url_only)


if __name__ == "__main__":
    main()
