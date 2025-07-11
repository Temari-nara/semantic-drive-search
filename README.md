# 📄 AI-Powered Semantic Document Search (Google Drive + Qdrant)

This project lets you **intelligently search documents stored in your Google Drive** using semantic similarity (powered by embeddings) — not just keyword match. It supports:

- ✅ Google Drive API (to fetch documents)
- ✅ Sentence Transformers (`MiniLM`) for generating embeddings
- ✅ Qdrant (Vector DB) to store and search vectors
- ✅ FastAPI backend for `/search` and `/sync`
- ✅ Streamlit frontend for a simple and clean UI

---

## ✨ Features

- 🔐 Google OAuth2 login for secure Drive access
- 📂 Supports `.pdf`, `.txt`, `.csv`, `.png` (OCR)
- 🧠 Fast semantic search via vector embeddings
- 📡 Real-time vector indexing with Qdrant
- 🔍 Incremental sync (only new files are indexed)
- 🖼️ Streamlit UI for search and sync
- 🛠️ Configurable via `.env`

---

## ⚙️ Prerequisites

- Google Cloud account (for Drive API)
- Qdrant Cloud account
- Git + terminal access

---

## 🛠️ Setup Instructions

### 1. 📥 Clone the Repository

```bash
git clone https://github.com/Temari-nara/Doc_Search_Cloud_Storage.git
cd Doc_Search_Cloud_Storage
2. 🐍 Create and Activate Virtual Environment
🪟 On Windows:

python -m venv venv
venv\Scripts\activate

🍎 On macOS / Linux:

python3 -m venv venv
source venv/bin/activate

3. 📦 Install Requirements
pip install -r requirements.txt

4. 🔐 Set Up Google Drive API Access
Follow these steps to create credentials.json:

Visit Google Cloud Console

Create a new project (e.g., SemanticSearch)

Go to APIs & Services → Library

Search and enable Google Drive API

Go to APIs & Services → Credentials

Click “+ CREATE CREDENTIALS” → “OAuth Client ID”

Choose Application Type: Desktop App

Download the credentials.json file

Place it in the project root

✅ On first run, the app will open a browser and prompt for Google login.
It will then auto-generate token.json (user access token).



5. 📁 Get Google Drive Folder ID (2 Options)
✅ Option A: From Streamlit UI
Run the UI: streamlit run ui/app.py

Click "🔄 Load My Folders" in the sidebar

Select a folder → it will display the folder ID to copy into .env

🔍 Option B: From Terminal

python helper_list_folders.py
You’ll see:
📁 Your Folders:
Name: Invoices | ID: 1AbCdEfGhIjK...
Name: HR Docs | ID: 1XyZ123...
Copy the desired folder ID.

6. 🔐 Set Up Qdrant Cloud
Visit Qdrant Cloud

Create a Sandbox Cluster

Copy your:

QDRANT_URL

QDRANT_API_KEY

7. ⚙️ Create .env File
In your root directory, create a .env file:

DRIVE_FOLDER_ID=your-google-drive-folder-id
QDRANT_URL=https://your-cluster.qdrant.cloud
QDRANT_API_KEY=your-qdrant-api-key

8. 📂 Upload Documents to Google Drive
Place your .pdf, .txt, .csv, or .png files in the Drive folder you selected above.

✅ No need to upload files locally.

9. 🔄 Sync Documents from Drive (2 Options)
🖱️ Option A: From Streamlit UI
Open the app with:
streamlit run ui/app.py

In the sidebar, click “🔄 Sync Documents”

This will:

Fetch new files

Parse and embed content

Store vectors in Qdrant

✅ Already indexed files will be skipped (incremental sync)

🔗 Option B: Use Sync API

curl -X POST http://localhost:8000/sync
Returns:

Edit
{ "message": "Sync started – check logs for progress." }
✅ This runs in the background — non-blocking.

10. 🚀 Start the FastAPI Backend
uvicorn search_service.api.main:app --reload
Open http://localhost:8000/docs to view and test:

GET /search?q=your_query

POST /sync

11. 🖼️ Use the Streamlit UI (Optional but Friendly)
streamlit run ui/app.py
Go to: http://localhost:8501

Enter your query to search semantically

Get file name, Drive link, and a content preview

🔍 Sample Output
{
  "results": [
    {
      "file_name": "loan_policy.pdf",
      "file_url": "https://drive.google.com/file/d/...",
      "preview": "This document outlines the policy regarding interest rates..."
    }
  ]
}

📁 Folder Structure

project-root/
├── .env
├── credentials.json
├── token.json  ← auto-generated
├── helper_list_folders.py
├── test_drive.py
├── requirements.txt
├── README.md
├── search_service/
│   ├── api/
│   │   └── main.py
│   ├── cloud/
│   │   └── google_drive_client.py
│   ├── parser/
│   │   └── [csv|txt|pdf|image]_parser.py
│   ├── index/
│   │   └── qdrant_indexer.py
│   └── embedding/
│       └── local_embedder.py
└── ui/
    └── app.py
    
💡 Future Enhancements
🗂️ Multi-folder recursive indexing

🔍 Filtered search by file type, folder, or tags

🧠 LLM-based summarization or Q&A (e.g., OpenAI/Gemini)

🔐 API authentication layer

☁️ Deploy on Hugging Face, EC2, or Azure App Service

👩‍💻 Developed By
Kavitha Jain
AI Engineer & Architect
📧 kavijain1011@gmail.com
🔗 [LinkedIn] (https://www.linkedin.com/in/kavita-jain-b88ab11ba/)