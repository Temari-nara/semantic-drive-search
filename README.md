#  AI-Powered Semantic Document Search (Google Drive + Qdrant)

This project allows you to **intelligently search documents** stored in your Google Drive using **semantic similarity** (not just keyword match). It uses:

- ✅ Google Drive API (to fetch files)
- ✅ Sentence Transformers (`MiniLM`) for embedding document text
- ✅ Qdrant (Vector DB) to store embeddings + metadata
- ✅ FastAPI for RESTful `/search` endpoint
- ✅ Streamlit (optional) for a simple web UI

---

## 📦 Features

- 🔐 Secure Google Drive access
- 📂 Supports `.pdf`, `.txt`, `.csv`, and `.png` (OCR)
- 🧠 Semantic embedding with `sentence-transformers`
- 📡 Search powered by **Qdrant vector similarity**
- 🖼️ Returns file name, Drive link, and content preview
- 🎯 Easily configurable with `.env`

---

## ⚙️ Prerequisites

- Python 3.8+
- Google Cloud account (for Drive API)
- Qdrant Cloud account (for vector DB)
- Git + terminal access

---

## 🛠️ Setup Instructions

### 1. 📥 Clone the Project

```bash
git clone git clone https://github.com/Temari-nara/Doc_Search_Cloud_Storage.git
cd <project-folder>

### 2. 🐍 Set Up Virtual Environment
  🪟 On Windows:

  python -m venv venv
  venv\Scripts\activate

  🍎 On macOS / Linux:

  python3 -m venv venv
  source venv/bin/activate

### 3. 📦 Install Requirements

  pip install -r requirements.txt

### 4. 🔐 Set Up Google Drive API
  🔑 How to Set Up Google Drive API Credentials
  To allow the application to access your Google Drive, follow these steps to create your own credentials.json file:

  ✅ Step 1: Go to Google Cloud Console
  Visit: https://console.cloud.google.com/

  Sign in with your Google account

  ✅ Step 2: Create a New Project
  Click the project dropdown (top bar)

  Click “New Project”

  Give it a name like Semantic Search and click Create

  ✅ Step 3: Enable Google Drive API
  In the left sidebar, go to APIs & Services > Library

  Search for “Google Drive API”

  Click it, then click “Enable”

  ✅ Step 4: Create OAuth 2.0 Credentials
  Go to APIs & Services > Credentials

  Click “+ CREATE CREDENTIALS” > “OAuth client ID”

  If prompted, configure the OAuth consent screen:

  Choose External, click Create

  Fill in the App name (e.g., DocSearchApp)

  Add your email for support and developer contact

  Click Save and Continue until you reach the final step

  Then:

  Choose Application type = Desktop App

  Name it (e.g., Drive Desktop Client)

  Click Create

  ✅ Step 5: Download credentials.json
  After creating the client, click Download JSON

  Rename the file to credentials.json if needed

  Move it to the root folder of this project

  ✅ Done! The first time you run the app, it will open a browser to authenticate and auto-generate token.json.

  ✅ On first run, the app will prompt login and generate token.json

  Please Note*
  🔐 Google Authentication
  When you run the app for the first time, it will:

  Open a browser window

  Ask you to log in with your Google account

  Request access to your Drive folder

  ✅ After login, it will auto-generate a token.json file on your machine

  Note: You do not need to create token.json manually. Just run python test_drive.py or trigger /sync, and it will be created after successful login.

  

### 5. 🔍 Get Your Google Drive Folder ID
  Run the helper script to list all folders in your Google Drive:
  python helper_list_folders.py
  Output:


  📁 Your Folders:

  Name: Invoices | ID: 1AbCdEfGhIjK...
  Name: HR Docs | ID: 1XyZ123...
  Choose a folder and copy its ID.

### 6. 🔐 Set Up Qdrant Cloud
  Go to https://cloud.qdrant.io

  Sign up and create a new Sandbox cluster

  Copy the Cluster URL (e.g., https://abc123.qdrant.cloud)

  Go to API Keys → create one → copy it

### 7. ⚙️ Create .env File
  Create a .env file in the root directory and add:

  env

  DRIVE_FOLDER_ID=your-google-drive-folder-id
  QDRANT_URL=https://your-qdrant-cluster.qdrant.cloud
  QDRANT_API_KEY=your-qdrant-api-key

### 8. 📂 Upload Documents to Drive
  Place supported files in your Drive folder:

  .pdf

  .txt

  .csv

  .png (will use OCR)

### 9. 🚀 Index the Files

  python test_drive.py
  ✅ This will:

  Fetch all files from the folder

  Parse and embed text

  Store in Qdrant Cloud
### 10. 🔍 Start the Search API” (with Postman step)

  Start the FastAPI server using:

  ```bash
  uvicorn search_service.api.main:app --reload
  Once running, visit the interactive Swagger UI:


  http://localhost:8000/docs
  You can test the /search endpoint from here.

  🧪 (Optional) Test the API in Postman
  Open Postman

  Create a new GET request

  Use the following URL:


  http://localhost:8000/search?q=your_query
  For example:


  http://localhost:8000/search?q=loan policy
  Click Send

  ✅ You’ll receive a JSON response with:

  Matching file names

  Their Google Drive URLs

  A preview snippet from each document


  [
    {
      "file_name": "loan_policy.pdf",
      "file_url": "https://drive.google.com/...",
      "preview": "This document covers the repayment and interest terms..."
    },
    ...
  ]

### 12. 🔄 Sync Newly Added Documents
  After uploading a new file to your configured Drive folder, you can sync it without restarting the app or re-running the script.

  This project supports incremental sync, which means:

  ✅ Already indexed files are skipped

  ✅ Only new documents are embedded and stored

  🖱️ Option 1: Click “🔄 Sync Documents” in Streamlit
  In the Streamlit sidebar:

  Click “🔄 Sync Documents”

  This will:

  Fetch new files from Drive

  Parse and embed content

  Store vectors in Qdrant

  You’ll see a success message like:

  Sync kicked off! Refresh results in ~1–2 min.

  🔗 Option 2: Trigger Sync via API
  You can also hit the sync endpoint using curl, Postman, or any HTTP client:


  curl -X POST http://localhost:8000/sync
  Response:

  { "message": "Sync started – check logs for progress." }
  ✅ This uses FastAPI BackgroundTasks so the server stays responsive.

### 12. (Optional) 🖼️ Run the Streamlit UI

  streamlit run ui/app.py
  Open your browser at:


  http://localhost:8501
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
├── token.json
├── test_drive.py
├── helper_list_folders.py
├── requirements.txt
├── README.md
├── search_service/
│   ├── api/
│   │   └── main.py
│   ├── cloud/
│   │   └── google_drive_client.py
│   ├── parser/
│   │   └── [csv, pdf, txt, image]_parser.py
│   ├── index/
│   │   └── qdrant_indexer.py
│   └── embedding/
│       └── local_embedder.py
└── ui/
    └── app.py  # Streamlit UI


💡 Future Enhancements
🗂️ Multi-folder recursive indexing

🔍 Filtered search by file type or folder

🧠 Integrate LLM (e.g., GPT) for Q&A

🔐 Secure API with authentication

☁️ Deploy on Hugging Face, EC2, or Azure

👩‍💻 Developed by
Kavita Jain
AI Engineer & Architect
🌐 https://www.linkedin.com/in/kavita-jain-b88ab11ba/
📧 kavijain1011@gmail.com






