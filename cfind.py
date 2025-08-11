import os
import re
import argparse
import fnmatch
import sys
import subprocess
import shlex
from rich.console import Console
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

console = Console()

def search_files(path=".", file_type=None, name_pattern=None, content_pattern=None):
    results = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_type and not file.lower().endswith(file_type.lower()):
                continue
            if name_pattern:
                if not (re.search(name_pattern, file, re.IGNORECASE) or 
                        fnmatch.fnmatch(file.lower(), f"*{name_pattern.lower()}*")):
                    continue
            content_matches = []
            if content_pattern:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line_num, line in enumerate(lines, 1):
                            if re.search(content_pattern, line, re.IGNORECASE):
                                content_matches.append((line_num, line.rstrip()))
                    if not content_matches:
                        continue
                except:
                    continue
            results.append((file_path, content_matches))
    return results

def extended_abspath(path):
    """Gibt einen vollständig aufgelösten, absoluten Pfad zurück."""
    path = os.path.realpath(
        os.path.abspath(
            os.path.expandvars(
                os.path.expanduser(path)
            )
        )
    )

    if path.startswith("~"):
        path = os.path.expanduser(path)
    
    if path.startswith("."):
        path = os.path.cwd() + os.sep + path.lstrip(".")

    if os.name == "nt":  # Windows
        path = path.replace("/", "\\")
    return path

def execute_command(command, file_path):
    """Cross-platform command execution with {} placeholder for file path."""

    print(f"\n[dim]Executing command:[/dim] {command} on {file_path}")
    try:
        # Pfad vollständig auflösen
        file_path = extended_abspath(file_path)

        if os.name == "nt":  # Windows
            quoted_path = f'"{file_path}"'
            cmd = command.replace("{}", quoted_path)
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30
            )
        else:  # Linux / macOS
            quoted_path = shlex.quote(file_path)
            cmd = command.replace("{}", quoted_path)
            result = subprocess.run(
                ["/bin/sh", "-c", cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30
            )

        console.print(f"[dim]Executing:[/dim] {cmd}")

        if result.stdout:
            console.print(f"[green]Output:[/green] {result.stdout.strip()}")
        if result.stderr:
            console.print(f"[red]Error:[/red] {result.stderr.strip()}")
        if result.returncode != 0:
            console.print(f"[yellow]Return code:[/yellow] {result.returncode}")
        console.print("─" * 30)
        
        return result.returncode == 0

    except subprocess.TimeoutExpired:
        console.print(f"[red]Command timed out: {cmd}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Error executing command '{cmd}': {e}[/red]")
        return False



def display_results(results, content_pattern=None, exec_command=None):
    if not results:
        console.print("[yellow]No files found matching the criteria.[/yellow]")
        return
    console.print(f"\n[green]Found {len(results)} file(s):[/green]\n")
    for file_path, content_matches in results:
        console.print(f"[bold blue]📁 {file_path}[/bold blue]")
        if exec_command:
            execute_command(exec_command, file_path)
        if content_matches and content_pattern:
            for line_num, line in content_matches:
                highlighted_line = Text()
                display_line = line.expandtabs(4)
                matches = list(re.finditer(content_pattern, display_line, re.IGNORECASE))
                last_end = 0
                for match in matches:
                    highlighted_line.append(display_line[last_end:match.start()])
                    highlighted_line.append(match.group(), style="bold red on yellow")
                    last_end = match.end()
                highlighted_line.append(display_line[last_end:])
                console.print(f"  [dim]Line {line_num:4d}:[/dim] ", end="")
                console.print(highlighted_line)
            console.print()
        else:
            console.print()

def interactive_mode():
    console.print("[bold cyan]Find Tool - Interactive Mode[/bold cyan]")
    console.print("[dim]Press Enter to skip any parameter[/dim]\n")
    file_type = console.input("File type (e.g., .py, .txt): ").strip() or None
    name_pattern = console.input("Name pattern (regex or substring): ").strip() or None
    content_pattern = console.input("Content pattern (regex or substring): ").strip() or None

    # Use prompt_toolkit for path input with autocompletion
    path_completer = PathCompleter(expanduser=True)
    search_path = prompt("Search path (default: current directory): ", completer=path_completer).strip() or "."
    exec_command = console.input("Execute command (use {} for file path): ").strip() or None
    return search_path, file_type, name_pattern, content_pattern, exec_command

def main():
    parser = argparse.ArgumentParser(description="Easy-to-use file finder tool")
    parser.add_argument("path", nargs="?", default=".", help="Search path")
    parser.add_argument("-t", "--type", help="File type/extension")
    parser.add_argument("-n", "--name", help="Name pattern (regex or substring)")
    parser.add_argument("-c", "--content", help="Content pattern (regex or substring)")
    parser.add_argument("-e", "--exec", dest="execute", help="Execute command on each found file (use {} as placeholder)")
    args = parser.parse_args()

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and args.path == "."):
        search_path, file_type, name_pattern, content_pattern, exec_command = interactive_mode()
    else:
        search_path, file_type, name_pattern, content_pattern, exec_command = (
            args.path, args.type, args.name, args.content, args.execute
        )

    console.print(f"\n[bold]Searching in:[/bold] {os.path.abspath(search_path)}")
    if file_type:
        console.print(f"[bold]File type:[/bold] {file_type}")
    if name_pattern:
        console.print(f"[bold]Name pattern:[/bold] {name_pattern}")
    if content_pattern:
        console.print(f"[bold]Content pattern:[/bold] {content_pattern}")
    if exec_command:
        console.print(f"[bold]Execute command:[/bold] {exec_command}")
    console.print("─" * 50)

    try:
        results = search_files(search_path, file_type, name_pattern, content_pattern)
        display_results(results, content_pattern, exec_command)
    except FileNotFoundError:
        console.print(f"[red]Error: Path '{search_path}' not found.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
