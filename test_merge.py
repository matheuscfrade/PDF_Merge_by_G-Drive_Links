from pypdf import PdfWriter
from pdf_utils import merge_pdfs
import os

def create_dummy_pdf(filename):
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(filename, "wb") as f:
        writer.write(f)

def test_merge():
    print("Creating dummy PDFs...")
    create_dummy_pdf("test1.pdf")
    create_dummy_pdf("test2.pdf")
    
    print("Merging PDFs...")
    success, msg = merge_pdfs(["test1.pdf", "test2.pdf"], "merged_test.pdf")
    
    if success:
        print("Success: PDFs merged.")
        if os.path.exists("merged_test.pdf"):
            print("Verified: Output file exists.")
        else:
            print("Error: Output file missing.")
    else:
        print(f"Failed: {msg}")

    # Cleanup
    try:
        os.remove("test1.pdf")
        os.remove("test2.pdf")
        os.remove("merged_test.pdf")
        print("Cleanup complete.")
    except:
        pass

if __name__ == "__main__":
    try:
        test_merge()
    except ImportError:
        print("pypdf not installed. Skipping test.")
    except Exception as e:
        print(f"Test failed with error: {e}")
