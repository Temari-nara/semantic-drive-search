import os
from dotenv import load_dotenv
from cloud.google_drive_client import GoogleDriveClient
from parser.file_parser_factory import FileParserFactory
from search_service.embedding.local_embedder import LocalEmbedder       # ← fixed
from search_service.index.qdrant_indexer import QdrantIndexer  

load_dotenv()
_q_url = os.getenv("QDRANT_URL")
_q_key = os.getenv("QDRANT_API_KEY")

drive_client = GoogleDriveClient(credentials_path='credentials.json')
embedder = LocalEmbedder()
indexer  = QdrantIndexer(url=_q_url, api_key=_q_key)

# def run_full_sync():
#     """Download, embed, and upsert all (new) docs."""
#     files = drive_client.list_supported_files()
#     print(f"[SYNC] Found {len(files)} files to (re)index…")

#     for f in files:
#         file_id, file_name = f["id"], f["name"]
#         path  = drive_client.download_file(file_id, file_name)

#         parser = FileParserFactory.get_parser(file_name)
#         if not parser:
#             print(f"[SYNC] Skipping unsupported type: {file_name}")
#             continue

#         content = parser.parse(path)
#         vector  = embedder.embed_text(content)

#         indexer.index_document(
#             vector=vector,
#             file_name=file_name,
#             content=content,
#             file_url=f["webViewLink"],
#             folder=f.get("folder", "Unknown")
#         )
#         print(f"[SYNC] ✅ Indexed {file_name}")


def run_full_sync():
    files = drive_client.list_supported_files()
    existing_ids = indexer.get_indexed_file_ids()

    new_files = [f for f in files if f["id"] not in existing_ids]
    print(f"[SYNC] Found {len(new_files)} new file(s) to index.")

    for f in new_files:
        file_id = f["id"]
        file_name = f["name"]
        path = drive_client.download_file(file_id, file_name)

        parser = FileParserFactory.get_parser(file_name)
        if not parser:
            print(f"[SKIP] Unsupported file: {file_name}")
            continue

        content = parser.parse(path)
        vector = embedder.embed_text(content)

        indexer.index_document(
            vector=vector,
            file_name=file_name,
            content=content,
            file_url=f["webViewLink"],
            folder=f.get("folder", "Unknown"),
            file_id=file_id  # ← pass it here for future checks
        )
        print(f"[✅] Indexed: {file_name}")
