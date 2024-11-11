import subprocess
import argparse
from bs4 import BeautifulSoup
import pyperclip


def fetch_url(url):
    result = subprocess.run(["curl", url], capture_output=True, text=True)
    return BeautifulSoup(result.stdout, 'html.parser')


def extract_pip_command(soup):
    pip_command = soup.find(id="pip-command")
    if pip_command:
        return pip_command.get_text(strip=True)
    return None


def pypi_search(query, install=False):
    url = f"https://pypi.org/project/{query}/"
    soup = fetch_url(url)
    command_text = extract_pip_command(soup)

    if command_text:
        pyperclip.copy(command_text)
        if install:
            subprocess.run(["pip", "install", query])
        return command_text
    else:
        url = f'https://pypi.org/search/?q={query}'
        soup = fetch_url(url)
        first_result = soup.find("a", class_="package-snippet")

        if first_result:
            href = first_result["href"]
            url = f"https://pypi.org{href}"
            soup = fetch_url(url)
            command_text = extract_pip_command(soup)

            if command_text:
                pyperclip.copy(command_text)
                if install:
                    subprocess.run(["pip", "install", query])
                return command_text
        return "No results found."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search PyPI and optionally install the package.")
    parser.add_argument("query", type=str,
                        help="The package name to search for")
    parser.add_argument("-i", "--install", action="store_true",
                        help="Flag to install the package")
    args = parser.parse_args()

    output = pypi_search(args.query, args.install)
    print(output)
