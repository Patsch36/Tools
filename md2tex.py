import markdown
import pypandoc
import os
import re
import argparse


template = r"""
\documentclass [11pt, halfparskip] {scrartcl}

\usepackage{ucs}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[ngerman]{babel}

\usepackage{amsmath,amssymb,amstext}
\usepackage[sfdefault,scaled=.85]{FiraSans}
\usepackage{newtxsf}

\usepackage{hyperref}

\usepackage{tabularx}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}} % linksbündig mit Breitenangabe
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}} % zentriert mit Breitenangabe
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}} % rechtsbündig mit Breitenangabe

\usepackage{multicol}

\usepackage{longtable}
\usepackage{booktabs}

\RedeclareSectionCommand[
  beforeskip=18pt,
  afterskip=-0pt,
  runin=false,
]{section}

\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

\usepackage[headtopline=1pt, headsepline=.5pt, footbotline=1pt, footsepline=.5pt]{scrlayer-scrpage}
\pagestyle{scrheadings}

\title{}
\subtitle{}
\author{Patrick Scheich}
\date{\today{}, Strümpfelbach}

\ihead{}
\ohead{}
\chead{Stand \today}

\ifoot{\headmark}
\automark{section}
\cfoot{}
\ofoot{Seite \pagemark}



\begin{document}

  \begin{titlepage}
      \maketitle
      \thispagestyle{empty}
      \setcounter{page}{0}
  \end{titlepage}
  
  \tableofcontents

  $$CONTENT$$

\end{document}"""


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

    tex_content = template.replace('$$CONTENT$$', tex_content)

    # Schreibe den TeX-Inhalt in die Ausgabedatei
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(tex_content)


def convert_tex_to_pdf(tex_file, pdf_file):
    pypandoc.convert_file(tex_file, 'pdf', outputfile=pdf_file)


if __name__ == "__main__":
    # Beispiel für die Verwendung
    parser = argparse.ArgumentParser(description='Convert Markdown to TeX.')
    parser.add_argument('input_file', type=str,
                        help='Path to the input Markdown file')
    parser.add_argument('output_file', type=str, nargs='?', default='output.tex',
                        help='Path to the output TeX file (default: output.tex)')
    parser.add_argument('--pdf', action='store_true',
                        help='Convert the output TeX file to PDF')
    args = parser.parse_args()

    convert_markdown_to_tex(args.input_file, args.output_file)
    print(f"Konvertierung abgeschlossen: {
          args.input_file} -> {args.output_file}")

    if args.pdf:
        pdf_file = os.path.splitext(args.output_file)[0] + '.pdf'
        convert_tex_to_pdf(args.output_file, pdf_file)
        print(f"PDF-Datei erstellt: {pdf_file}")
