from rich.console import Console
from rich.markdown import Markdown
import argparse
import sys


def render_markdown(file_path: str):
    """
    Render a Markdown file to the terminal using the Rich package.

    :param file_path: Path to the Markdown file to render
    """
    console = Console()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
        # Create a Markdown renderable object
        markdown = Markdown(markdown_content)
        # Print the rendered Markdown to the console
        console.print(markdown)
    except FileNotFoundError:
        console.print(
            f"[bold red]Error:[/bold red] File '{file_path}' not found.")
    except PermissionError:
        console.print(
            f"[bold red]Error:[/bold red] Permission denied for file '{file_path}'.")
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Render a Markdown file to the terminal.")
    parser.add_argument("file_path", type=str,
                        help="Path to the Markdown file to render")
    args = parser.parse_args()

    render_markdown(args.file_path)
