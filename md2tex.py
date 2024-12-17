import markdown
import pypandoc
import os
import re


def preprocess_markdown(content):
    """
    Konvertiert 2-Leerzeichen-Einrückungen zu 4-Leerzeichen-Einrückungen
    für Listen.
    """
    # Ersetze Zeilen mit 2-Leerzeichen-Einrückung zu 4-Leerzeichen-Einrückung
    content = re.sub(r'(?<=\n)( {2,})(- )', lambda match: ' ' *
                     (len(match.group(1)) * 2) + match.group(2), content)
    return content


def convert_markdown_to_tex(markdown_file, tex_file, templatefile='Vorlage.tex'):
    # Lese die Markdown-Datei
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    markdown_content = preprocess_markdown(markdown_content)

    # Konvertiere Markdown zu HTML
    html_content = markdown.markdown(markdown_content, extensions=[
                                     'tables', 'fenced_code', 'toc'])

    # Konvertiere HTML zu TeX
    tex_content = pypandoc.convert_text(
        html_content, 'latex', format='html', extra_args=['--listings'])

    with open(templatefile, 'r', encoding='utf-8') as f:
        template = f.read()

    tex_content = template.replace('$$CONTENT$$', tex_content)

    # Schreibe den TeX-Inhalt in die Ausgabedatei
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(tex_content)


if __name__ == "__main__":
    # Beispiel für die Verwendung
    markdown_file = 'input.md'  # Pfad zur Markdown-Datei
    tex_file = 'output.tex'      # Pfad zur Ausgabedatei
    convert_markdown_to_tex(markdown_file, tex_file)
    print(f"Konvertierung abgeschlossen: {markdown_file} -> {tex_file}")
