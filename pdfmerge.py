import os
import sys
from PyPDF2 import PdfMerger

def merge_pdfs(folder_path, output_pdf):
    merger = PdfMerger()

    # Durchlaufe alle Dateien im angegebenen Ordner
    pdf_files_found = False
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            merger.append(pdf_path)
            pdf_files_found = True
            print(f"Added: {filename}")

    if not pdf_files_found:
        print("Error: No PDF files found in the specified folder.")
        sys.exit(1)

    # Speichere das zusammengeführte PDF
    if not output_pdf.endswith('.pdf'):
        output_pdf += '.pdf'

    merger.write(output_pdf)
    merger.close()
    print(f"All PDFs merged into {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_pdfs.py <folder_path> <output_pdf>")
        sys.exit(1)

    folder_path = sys.argv[1]
    output_pdf = sys.argv[2]

    merge_pdfs(folder_path, output_pdf)
