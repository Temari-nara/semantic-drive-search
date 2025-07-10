# search_service/index/qdrant_indexer.py

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

class QdrantIndexer:
    def __init__(self, collection_name="documents", url=None, api_key=None):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name

        # Create collection if it doesn't exist
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # 384 for MiniLM
            )

    def index_document(self, vector, file_name, content, file_url, file_id=None, folder="Unknown"):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "file_id": file_id,              # ✅ add file_id
                "file_name": file_name,
                "file_url": file_url,
                "content": content,
                "folder": folder                 # ✅ optional: for display
            }
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])
    
    def get_indexed_file_ids(self):
        file_ids = set()
        offset = None

        while True:
            response, next_offset = self.client.scroll(
                collection_name=self.collection_name,
                offset=offset,
                with_payload=True,
                limit=100
            )
            for point in response:
                file_id = point.payload.get("file_id")
                if file_id:
                    file_ids.add(file_id)

            if not next_offset:
                break
            offset = next_offset

        return file_ids


    def search(self, query_vector, top_k=3):
        result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        return result
