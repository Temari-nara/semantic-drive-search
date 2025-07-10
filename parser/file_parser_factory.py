# parser/file_parser_factory.py

from parser.txt_parser import TxtParser
from parser.csv_parser import CsvParser
from parser.pdf_parser import PdfParser
from parser.image_parser import ImageParser

class FileParserFactory:
    @staticmethod
    def get_parser(file_name: str):
        file_name = file_name.lower()
        if file_name.endswith('.txt'):
            return TxtParser
        elif file_name.endswith('.csv'):
            return CsvParser
        elif file_name.endswith('.pdf'):
            return PdfParser
        elif file_name.endswith('.png'):
            return ImageParser
        else:
            return None
