import streamlit as st
import os
import subprocess
import time
from t2 import unified_query

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(
    page_title="Semantic Data Explorer",
    layout="wide"
)

# --------------------------
# CUSTOM STYLING
# --------------------------

st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
}

/* Title */
h1 {
    text-align:center;
    font-size:42px;
    font-weight:700;
}

/* Card style */
.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:15px;
    backdrop-filter: blur(10px);
    margin-bottom:15px;
}

/* Chat bubbles */
.user {
    background:#1f4e79;
    padding:12px;
    border-radius:10px;
    margin-bottom:5px;
}

.bot {
    background:#162a40;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#1e90ff,#00c6ff);
    border:none;
    padding:10px 20px;
    border-radius:10px;
    color:white;
    font-weight:600;
}

.stButton>button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# TITLE
# --------------------------

st.title("📊 Semantic Data Explorer")
st.write("Upload documents and ask questions about them.")

# --------------------------
# SIDEBAR
# --------------------------

st.sidebar.header("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Select files",
    accept_multiple_files=True
)

# --------------------------
# INGEST BUTTON
# --------------------------

if st.sidebar.button("🚀 Process Documents"):

    if uploaded_files:

        progress = st.sidebar.progress(0)
        status = st.sidebar.empty()

        total = len(uploaded_files)

        for i, file in enumerate(uploaded_files):

            path = os.path.join(UPLOAD_DIR, file.name)

            with open(path, "wb") as f:
                f.write(file.getbuffer())

            progress.progress((i + 1) / total)
            status.write(f"Uploading {file.name}")

        st.sidebar.success("Files uploaded")

        with st.spinner("Indexing documents..."):

            subprocess.run(["python", "ingest.py", UPLOAD_DIR])

        progress.progress(1.0)
        status.write("Index complete")

        st.sidebar.success("Documents indexed")

    else:
        st.sidebar.warning("Upload files first")

# --------------------------
# CHAT
# --------------------------

st.header("💬 Ask Questions")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask something about your documents")

if st.button("Ask AI"):

    if query:

        with st.spinner("🔎 Searching knowledge base..."):

            answer = unified_query(query)

        st.session_state.history.append((query, answer))

# --------------------------
# DISPLAY CHAT
# --------------------------

for q, a in reversed(st.session_state.history):

    st.markdown(f'<div class="user">🧑 <b>You:</b> {q}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot">🤖 <b>AI:</b> {a}</div>', unsafe_allow_html=True)