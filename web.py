import argparse
import webbrowser
import pyperclip
from googlesearch import search
from tools.curses_wrapper import MenuSelector
import os
import requests
import sys
import signal

# File path for the acronym directory
ACRONYM_FILE_PATH = os.path.expanduser("~/.acronymes.txt")


class AcronymManager:
    """Manages acronyms and their URLs."""

    def __init__(self, file_path):
        self.file_path = file_path

    def resolve_acronym(self, acronym):
        """Reads an acronym and returns the associated URL."""
        acronym_parts = acronym.split(" ")
        acronyms = self._load_acronyms()
        matching_acronyms = [
            url for ac, url in acronyms.items()
            if all(part.lower() in ac.lower() for part in acronym_parts)
        ]
        if matching_acronyms:
            return matching_acronyms[0]
        else:
            print(f"No URL found for the acronym '{acronym}'.")
            return None

    def add_acronym(self, acronym, url):
        """Adds a new acronym with URL or overwrites it."""
        acronyms = self._load_acronyms()

        if acronym in acronyms:
            print(f"The acronym '{acronym}' already exists with the URL: {
                  acronyms[acronym]}")
            choice = input(
                "Do you want to overwrite it (o) or enter a new name (n)? ").strip().lower()
            if choice == 'n':
                acronym = input(
                    "Please enter a new name for the acronym: ").strip()
            elif choice != 'o':
                print("Invalid selection. Operation aborted.")
                return

        acronyms[acronym] = url
        self._save_acronyms(acronyms)
        print(f"Acronym '{acronym}' with the URL '{url}' has been added.")

    def delete_acronym(self, acronym=None):
        """Deletes an acronym by name or selection by the user."""
        acronyms = self._load_acronyms()

        if not acronyms:
            print("No acronyms available.")
            return

        if acronym:
            if acronym in acronyms:
                del acronyms[acronym]
                self._save_acronyms(acronyms)
                print(f"Acronym '{acronym}' has been deleted.")
            else:
                print(f"The acronym '{acronym}' does not exist.")
        else:
            selector = MenuSelector(
                sorted(acronyms.keys()), prompt="Select an acronym to delete:")
            selected_acronym = selector.select()
            if selected_acronym:
                del acronyms[selected_acronym]
                self._save_acronyms(acronyms)
                print(f"Acronym '{selected_acronym}' has been deleted.")

    def change_acronym(self):
        """Opens a Menu Selector to select an acroynm, then asks for new link"""
        acronyms = self._load_acronyms()
        acronym_keys = sorted(acronyms.keys())

        formatted_acronyms = [
            f"{key}: {acronyms[key]}" for key in acronym_keys]

        selected_acronym = MenuSelector(
            formatted_acronyms, prompt="Wählen Sie ein Acronym aus:").select().split(":")[0]
        inp = input(
            "Geben Sie die neue URL ein (cp um aus dem Copybuffer einzufügen, leer um alte URL zu behalten):")
        if inp == "cp":
            new_url = pyperclip.paste()
        elif inp != "":
            new_url = inp
        else:
            new_url = acronyms[selected_acronym]

        if new_url and not new_url.startswith(("http://", "https://")):
            new_url = "https://" + new_url

        # Test if the URL can be opened with https
        try:
            response = requests.head(new_url, allow_redirects=True)
            if response.status_code >= 400:
                print(f"Warning: The URL '{new_url}' might not be reachable (status code: {
                      response.status_code}). Trying http instead.")
            new_url = "http://" + new_url[8:]  # Replace https with http
            response = requests.head(new_url, allow_redirects=True)
            if response.status_code >= 400:
                print(f"Warning: The URL '{
                      new_url}' might not be reachable (status code: {response.status_code}).")
        except requests.RequestException as e:
            print(f"Error: The URL '{
                  new_url}' is not reachable. Exception: {e}")
        if new_url and not "www." in new_url:
            new_url = new_url.replace(
                "http://", "http://www.").replace("https://", "https://www.")

        # Test if the URL can be opened
        try:
            response = requests.head(new_url, allow_redirects=True)
            if response.status_code >= 400:
                print(f"Warning: The URL '{
                    new_url}' might not be reachable (status code: {response.status_code}).")
        except requests.RequestException as e:
            print(f"Error: The URL '{
                  new_url}' is not reachable. Exception: {e}")

        acronyms[selected_acronym] = new_url
        self._save_acronyms(acronyms)
        print(f"Acronym '{selected_acronym}' wurde geändert.")

    def select_acronym(self):
        """Allows the user to select an acronym and returns the associated URL."""
        acronyms = self._load_acronyms()
        selector = MenuSelector(sorted(acronyms.keys()),
                                prompt="Select an acronym:")
        selected_acronym = selector.select()
        return acronyms[selected_acronym] if selected_acronym else None

    def _load_acronyms(self):
        """Loads all saved acronyms and their URLs."""
        acronyms = {}
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    if ":" in line:
                        ac, url = line.strip().split(":", 1)
                        acronyms[ac] = url
        except FileNotFoundError:
            print(f"The file '{self.file_path}' was not found.")
        return acronyms

    def _save_acronyms(self, acronyms):
        """Saves the acronyms and URLs to the file."""
        with open(self.file_path, "w") as file:
            for ac, url in acronyms.items():
                file.write(f"{ac}:{url}\n")


class GoogleSearchHelper:
    """Helper class for Google search."""

    @staticmethod
    def perform_search(query, result_num=1, key_string=None, open_url=True):
        """Performs a Google search and opens or copies the result."""
        if result_num == 0 and key_string is None:
            search_url = f"https://www.google.com/search?q={query}"
            GoogleSearchHelper._handle_result(search_url, open_url)
            return

        results = list(search(query, num_results=10))

        if key_string:
            filtered_results = [url for url in results if key_string in url]
            if not filtered_results:
                print("No result found containing the key string.")
                return
            result_url = filtered_results[0]
        else:
            if result_num > len(results) or result_num < 1:
                print("Invalid result number.")
                return
            result_url = results[result_num - 1]

        GoogleSearchHelper._handle_result(result_url, open_url)

    @staticmethod
    def _handle_result(url, open_url):
        """Opens the URL or copies it to the clipboard."""
        if open_url:
            import subprocess
            subprocess.Popen(['brave', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Opening: {url}")
            os.kill(os.getppid(), signal.SIGTERM)
        else:
            pyperclip.copy(url)
            print(f"URL copied to clipboard: {url}")


def main():
    parser = argparse.ArgumentParser(
        description="Google search script with acronym management")
    parser.add_argument("-k", "--key", type=str,
                        help="Key string for filtering search results")
    parser.add_argument("-u", "--url_only", action="store_true",
                        help="Copy only the URL to the clipboard")
    parser.add_argument("-a", "--acronym", type=str, nargs="?",
                        const="", help="Acronym for direct URL resolution")
    parser.add_argument("-n", "--acronym_link", type=str,
                        help="URL for the acronym when creating a new one")
    parser.add_argument("-d", "--delete_acronym", type=str, nargs="?",
                        const="", help="Specify acronym to delete or select interactively")
    parser.add_argument("-c", "--change_acronym", action="store_true", default=False,
                        help="Specify the acronyme to change.")
    parser.add_argument("search_term", nargs="?", default=None,
                        help="The search term for Google or the result number")
    parser.add_argument("result_num", nargs="?", default=0,
                        help="The result number or the key string")

    args = parser.parse_args()
    acronym_manager = AcronymManager(ACRONYM_FILE_PATH)

    if args.acronym_link:
        if not args.acronym:
            print("Acronym is missing.")
            return
        acronym_manager.add_acronym(args.acronym, args.acronym_link)

    elif args.delete_acronym is not None:
        acronym_manager.delete_acronym(args.delete_acronym)
    elif args.change_acronym is True:
        acronym_manager.change_acronym()

    elif args.acronym is not None:
        if args.acronym.strip() == "":
            url = acronym_manager.select_acronym()
            if url:
                GoogleSearchHelper._handle_result(url, not args.url_only)
        else:
            url = acronym_manager.resolve_acronym(args.acronym)
            if url:
                GoogleSearchHelper._handle_result(url, not args.url_only)
            else:
                print(f"No URL found for the acronym '{args.acronym}'.")

    else:
        query = pyperclip.paste() if args.search_term is None else args.search_term
        result_num = int(args.result_num) if str(
            args.result_num).isdigit() else 1
        GoogleSearchHelper.perform_search(
            query, result_num, args.key, not args.url_only)


if __name__ == "__main__":
    main()
