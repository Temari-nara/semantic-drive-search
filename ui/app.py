import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"        # FastAPI base URL

st.set_page_config(page_title="Semantic Document Search", layout="centered")

# ──────────────────────────────────────────────────────────────
# Load Folder and folder_id
# ──────────────────────────────────────────────────────────────

st.sidebar.title("📁 Google Drive Folder Explorer")

# Step 1: Fetch folders and store in session state
if "folders" not in st.session_state:
    st.session_state.folders = None

if st.sidebar.button("🔄 Load My Folders"):
    try:
        resp = requests.get("http://127.0.0.1:8000/list-folders", timeout=10)
        folders = resp.json()
        if not folders:
            st.sidebar.warning("No folders found.")
        else:
            st.session_state.folders = folders
            st.sidebar.success("Folders loaded!")
    except Exception as e:
        st.sidebar.error(f"Failed to load folders: {e}")

# Step 2: Show dropdown only if folders are loaded
if st.session_state.folders:
    folder_options = {f["name"]: f["id"] for f in st.session_state.folders}
    selected_name = st.sidebar.selectbox("Select a folder:", list(folder_options.keys()))
    selected_id = folder_options[selected_name]

    st.sidebar.markdown("### 📌 Folder ID:")
    st.sidebar.code(selected_id)

    st.sidebar.success("Copy this ID into your `.env` as `DRIVE_FOLDER_ID`")



# ──────────────────────────────────────────────────────────────
# Sidebar – Sync button
# ──────────────────────────────────────────────────────────────
st.sidebar.title("⚙️ Maintenance")

if st.sidebar.button("🔄  Sync Documents"):
    with st.sidebar:
        st.write("Starting sync…")
    try:
        resp = requests.post(f"{API_BASE}/sync", timeout=5)
        if resp.status_code == 202:
            st.sidebar.success("Sync kicked‑off! Refresh results in ~1–2 min.")
        else:
            st.sidebar.error(f"Sync failed: {resp.text}")
    except Exception as sync_err:
        st.sidebar.error(f"Couldn’t reach the API: {sync_err}")

# ──────────────────────────────────────────────────────────────
# Main UI – Search
# ──────────────────────────────────────────────────────────────
st.title("📄 Semantic Search in Google Drive")
st.write("Search documents using AI‑powered embeddings.")

query = st.text_input("Enter your search query")

if query:
    with st.spinner("Searching…"):
        try:
            resp = requests.get(f"{API_BASE}/search", params={"q": query})
            resp.raise_for_status()
            results = resp.json().get("results", [])
            if not results:
                st.warning("No matching documents found.")
            else:
                for r in results:
                    st.subheader(r["file_name"])
                    st.markdown(f"[🔗 View on Drive]({r['file_url']})")
                    st.code(r["preview"], language="text")
        except Exception as e:
            st.error(f"❌ API error: {e}")
