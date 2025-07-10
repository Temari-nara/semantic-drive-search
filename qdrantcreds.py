from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://fe3fb69d-7252-4712-bea2-8f330aa3c42d.eu-west-2-0.aws.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.nDfLwT6DVgBPg93vQcpoLM4IkYbZAY-Sx6spflHFS9A",
)

print(qdrant_client.get_collections())