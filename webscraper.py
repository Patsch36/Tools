import requests
import pyperclip
import argparse
from bs4 import BeautifulSoup

def scrape_and_copy(url):
    try:
        # HTTP-Anfrage an die angegebene URL senden
        response = requests.get(url)
        response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war

        # HTML-Code analysieren und die <style> und <script> Tags entfernen
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Entferne <style> und <script> Tags
        for script in soup(["script", "style"]):
            script.decompose()  # Entferne die Tags

        # Den bereinigten HTML-Code in die Zwischenablage kopieren
        html_code = str(soup)
        pyperclip.copy(html_code)
        print("HTML-Code (ohne <style> und <script>-Tags) wurde in die Zwischenablage kopiert.")

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der URL: {e}")

if __name__ == "__main__":
    # ArgumentParser erstellen
    parser = argparse.ArgumentParser(description="Scrape HTML code from a URL and copy it to the clipboard.")
    parser.add_argument("url", type=str, help="Die URL, die gescraped werden soll.")
    
    # Argumente parsen
    args = parser.parse_args()
    
    # Scraping und Kopieren in die Zwischenablage
    scrape_and_copy(args.url)