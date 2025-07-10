from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="your-qdrant-url", 
    api_key="your-qdrant-api-key",
)

print(qdrant_client.get_collections())