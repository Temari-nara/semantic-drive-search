# test_drive.py

import os
from dotenv import load_dotenv
from cloud.google_drive_client import GoogleDriveClient
from parser.file_parser_factory import FileParserFactory
from search_service.embedding.local_embedder import LocalEmbedder
from search_service.index.qdrant_indexer import QdrantIndexer

def main():
    # Load environment variables from .env
    load_dotenv()
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    # Initialize components
    drive_client = GoogleDriveClient(credentials_path='credentials.json')
    embedder = LocalEmbedder()
    indexer = QdrantIndexer(url=qdrant_url, api_key=qdrant_api_key)

    print("🔍 Fetching files from your Google Drive folder...")
    files = drive_client.list_supported_files()

    if not files:
        print("⚠️  No supported files found.")
        return

    print(f"\n📄 Found {len(files)} supported file(s):\n")

    for file in files:
        file_id = file['id']
        file_name = file['name']
        print(f"→ Downloading {file_name} ...")
        path = drive_client.download_file(file_id, file_name)

        parser = FileParserFactory.get_parser(file_name)
        if parser:
            content = parser.parse(path)
            print(f"✅ Parsed {file_name}")

            # Embed and index in Qdrant
            vector = embedder.embed_text(content)
            indexer.index_document(
                vector=vector,
                file_name=file_name,
                content=content,
                file_url=file.get('webViewLink')
            )

            print(f"📌 Indexed: {file_name}\n")
        else:
            print(f"⚠️ No parser found for {file_name}\n")


if __name__ == "__main__":
    main()
