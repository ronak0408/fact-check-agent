import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from an uploaded PDF file.
    Args:
        pdf_file: The file object from streamlit's file_uploader
    Returns:
        str: Extracted text from all pages.
    """
    text = ""
    try:
        # Open the PDF from bytes
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"