# Enterprise RAG Knowledge Management Chatbot

## Overview

This project implements an enterprise knowledge management system powered by Retrieval-Augmented Generation (RAG). The application enables users to upload and query internal company documents using natural language while generating context-aware responses grounded in retrieved information.

The system supports multiple document formats, including PDF, Excel, CSV, PowerPoint, and text files, making it suitable for sales, marketing, and organizational knowledge management.

## Features

* Retrieval-Augmented Generation (RAG) based question answering
* Semantic search using Sentence Transformer embeddings
* Multi-format document ingestion (PDF, Excel, CSV, PPT, TXT)
* ChromaDB vector database for efficient document retrieval
* Google Gemini integration for context-aware response generation
* Streamlit-based interactive user interface
* Support for both structured and unstructured enterprise data

## System Architecture

The application consists of four major components:

1. Document ingestion and preprocessing
2. Semantic embedding generation
3. Vector storage and retrieval using ChromaDB
4. Context-aware response generation using Google Gemini

## Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| User Interface       | Streamlit             |
| Vector Database      | ChromaDB              |
| Embedding Model      | Sentence Transformers |
| Large Language Model | Google Gemini         |
| Data Processing      | Pandas, NumPy         |
| Document Processing  | PyPDF2, python-pptx   |

## Project Structure

```
enterprise-rag-chatbot/
│
├── app.py
├── ingest.py
├── t2.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Chethana131/enterprise-rag-chatbot.git
cd enterprise-rag-chatbot
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables:

```
GEMINI_API_KEY=<your_api_key>
```

Run the application:

```bash
streamlit run app.py
```

## Methodology

The system follows a Retrieval-Augmented Generation pipeline:

* Documents are uploaded and preprocessed.
* Text is extracted and divided into semantic chunks.
* Sentence Transformer embeddings are generated.
* Embeddings are stored in ChromaDB.
* User queries are converted into embeddings and matched against the vector database.
* Retrieved context is supplied to Google Gemini to generate grounded responses.

## Applications

* Enterprise knowledge management
* Sales and marketing intelligence
* Internal document search
* Semantic document retrieval
* Decision support systems

## Future Enhancements

* Authentication and role-based access control
* Voice-enabled interaction
* Multi-user collaboration
* Dashboard for document analytics
* Cloud deployment and scalability improvements

## Authors

Developed as a Mini Project for the School of Computer Science and Engineering, RV University.
