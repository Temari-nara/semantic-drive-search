# search_service/api/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from search_service.embedding.local_embedder import LocalEmbedder
from search_service.index.qdrant_indexer import QdrantIndexer
from fastapi import BackgroundTasks
from search_service.pipeline.sync_pipeline import run_full_sync   # new helper we’ll create

app = FastAPI(title="Document Search API")

# Load .env
load_dotenv()
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

# Initialize components
embedder = LocalEmbedder()
indexer = QdrantIndexer(url=qdrant_url, api_key=qdrant_api_key)

@app.get("/search")
def search_documents(q: str = Query(..., description="Your search query")):
    query_vector = embedder.embed_text(q)
    results = indexer.search(query_vector, top_k=3)

    response = []
    for r in results:
        payload = r.payload
        response.append({
            "file_name": payload["file_name"],
            "file_url": payload["file_url"],
            "preview": payload["content"][:300] + "...", # optional preview
            "folder": payload.get("folder", "Unknown")
        })
    return {"results": response}


@app.post("/sync", status_code=202)
def sync_documents(background_tasks: BackgroundTasks):
    """
    Re‑index the Google‑Drive folder:
    - Downloads any (new) supported files
    - Parses + embeds their content
    - Upserts into Qdrant
    """
    # run in background so the HTTP call returns immediately
    background_tasks.add_task(run_full_sync)
    return {"message": "Sync started – check logs for progress."}
