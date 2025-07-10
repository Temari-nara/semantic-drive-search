# parser/csv_parser.py

import pandas as pd

class CsvParser:
    @staticmethod
    def parse(file_path: str) -> str:
        try:
            df = pd.read_csv(file_path)
            return df.astype(str).to_string(index=False)
        except Exception as e:
            print(f"Error parsing CSV: {file_path} - {e}")
            return ""
