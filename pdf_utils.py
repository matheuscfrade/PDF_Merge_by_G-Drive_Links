from pypdf import PdfWriter
import os

def merge_pdfs(file_list, output_path):
    """
    Merges a list of PDF files into a single PDF file.

    Args:
        file_list (list): List of file paths to merge.
        output_path (str): Path to save the merged PDF.
    """
    merger = PdfWriter()

    try:
        for credit, pdf in enumerate(file_list):
            # Verify if file exists
            if not os.path.exists(pdf):
                print(f"Error: File not found: {pdf}")
                continue
            
            # Simple check if it is a PDF
            if not pdf.lower().endswith('.pdf'):
                print(f"Warning: Skipping non-PDF file: {pdf}")
                continue

            merger.append(pdf)

        merger.write(output_path)
        merger.close()
        return True, "Merged successfully."
    except Exception as e:
        return False, f"Error merging PDFs: {str(e)}"
