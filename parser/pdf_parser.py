# parser/pdf_parser.py

import fitz  # PyMuPDF

class PdfParser:
    @staticmethod
    def parse(file_path: str) -> str:
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"Error parsing PDF: {file_path} - {e}")
            return ""
