# t2.py — Query Engine

import os
import chromadb
import re
from sentence_transformers import SentenceTransformer
from google import genai

DB_PATH = "./vector_db"
COLLECTION_NAME = "project_docs"
EMBED_MODEL = "all-MiniLM-L6-v2"


def extract_filename(query):

    words = re.findall(r"[A-Za-z0-9_\-\.]+", query.lower())

    for w in words:
        if "." in w:
            return w

    for w in words:
        if len(w) > 2:
            return w

    return None


def query_collection(client, embedding, n=6, ftype=None, filename=None):

    col = client.get_collection(name=COLLECTION_NAME)

    kwargs = {
        "query_embeddings": embedding.tolist(),
        "n_results": n
    }

    if ftype and filename:

        kwargs["where"] = {
            "$and": [
                {"type": ftype},
                {
                    "$or": [
                        {"filename": filename},
                        {"filename_noext": filename}
                    ]
                }
            ]
        }

    elif ftype:

        kwargs["where"] = {"type": ftype}

    elif filename:

        kwargs["where"] = {
            "$or": [
                {"filename": filename},
                {"filename_noext": filename}
            ]
        }

    res = col.query(**kwargs)

    docs = res.get("documents", [[]])[0]

    return docs


def unified_query(query):

    client = chromadb.PersistentClient(path=DB_PATH)

    embedder = SentenceTransformer(EMBED_MODEL)

    emb = embedder.encode([query])

    filename = extract_filename(query)

    # -------- NEW METADATA SEARCH --------
    file_meta_docs = query_collection(client, emb, 3, "file_meta", filename)
    # -------------------------------------

    excel_docs = query_collection(client, emb, 6, "excel_struct", filename)

    text_docs = query_collection(client, emb, 8, "text", filename)

    if not file_meta_docs and not excel_docs and not text_docs:

        file_meta_docs = query_collection(client, emb, 3, "file_meta")

        excel_docs = query_collection(client, emb, 6, "excel_struct")

        text_docs = query_collection(client, emb, 8, "text")

    context = "\n\n".join(file_meta_docs + excel_docs + text_docs)

    api_key = os.getenv("GEMINI_API_KEY")

    prompt = f"""

You are a data analyst and Sales and Marketting consultant expert answering questions about spreadsheets and documents.

Rules:

If a row contains the word "Total", treat it as a final value.
Do NOT sum rows again if totals already exist.

Use exact numbers when available.

When you give a value, ALSO mention where the value came from:
- file name
- sheet name
- table number if available

Example format:
Value: 300000  
Source: file=finance.xlsx, sheet=October, table=0

Context:
{context}

Question:
{query}

Answer clearly.
"""

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    import sys

    q = sys.argv[1]

    ans = unified_query(q)

    print("\nANSWER\n")

    print(ans)