# parser/txt_parser.py

class TxtParser:
    @staticmethod
    def parse(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error parsing TXT: {file_path} - {e}")
            return ""
