# # ui/app.py

# import requests
# import streamlit as st

# st.set_page_config(page_title="Semantic Document Search", layout="centered")

# st.title("📄 Semantic Search in Google Drive")
# st.write("Search documents using AI-powered embeddings.")

# query = st.text_input("Enter your search query")

# if query:
#     with st.spinner("Searching..."):
#         try:
#             response = requests.get("http://127.0.0.1:8000/search", params={"q": query})
#             data = response.json()

#             results = data.get("results", [])

#             if not results:
#                 st.warning("No matching documents found.")
#             else:
#                 for r in results:
#                     st.subheader(r['file_name'])
#                     st.markdown(f"[🔗 View on Drive]({r['file_url']})")
#                     st.code(r['preview'], language="text")
#         except Exception as e:
#             st.error(f"❌ Error: {e}")


#-==================================-
# ui/app.py
import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"        # FastAPI base URL

st.set_page_config(page_title="Semantic Document Search", layout="centered")

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
