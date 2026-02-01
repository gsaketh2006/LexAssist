# RAG - Legal Document Retrieval System

A Retrieval-Augmented Generation (RAG) system designed for legal document processing and querying, utilizing FAISS vector database for efficient document retrieval.

## 📋 Project Overview

This project implements an intelligent RAG pipeline for legal document analysis with advanced query processing capabilities:

- **Adaptive Query Rewriting**: Automatically expands vague queries into formal legal language
- **Dynamic Retrieval**: Intelligently determines optimal number of document chunks needed
- **Similarity Threshold Filtering**: Ensures only relevant context is used for answering
- **Hallucination Prevention**: Strict prompting ensures answers come only from retrieved documents
- **Interactive CLI**: Simple command-line interface for querying the knowledge base

## 🗂️ Project Structure

```
RAG/
├── data/                          # Data directory for raw documents
├── legal_faiss_db/                # FAISS vector database storage
│   ├── index.faiss               # FAISS index file
│   └── index.pkl                 # Serialized metadata
├── myenv/                         # Python virtual environment
├── .env                          # Environment variables (API keys, configs)
├── .gitignore                    # Git ignore rules
├── data_ingestion.py             # Document loading and processing
├── query.py                      # Query interface for RAG system
├── README.md                     # Project documentation
└── requirements.txt              # Python dependencies
```

## 🚀 Features

### Document Processing
- **PDF Extraction**: Automatic processing of legal PDFs from directory using PyMuPDF
- **Smart Chunking**: Recursive character-based splitting (250 char chunks, 50 char overlap)
- **Efficient Indexing**: FAISS vector store with HuggingFace embeddings

### Query Intelligence
- **Adaptive Query Rewriting**: Expands short/vague queries (≤4 words) into formal legal language
- **Dynamic K Selection**: LLM automatically determines optimal retrieval count (1-20 chunks)
- **Similarity Filtering**: Threshold-based filtering (cutoff: 2.3) to reject irrelevant results
- **Hallucination Prevention**: Responds with "I don't know" when answer isn't in context

### Technical
- **Zero Temperature LLM**: Deterministic responses for legal accuracy
- **Groq LLaMA 3.1**: Ultra-fast inference with llama-3.1-8b-instant model
- **Interactive CLI**: User-friendly command-line query interface
- **Secure Configuration**: Environment-based API key management

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RAG
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   
   # On Windows
   myenv\Scripts\activate
   
   # On macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configurations
   ```

### Getting API Keys

**Groq API Key** (Required):
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Add it to your `.env` file as `GROQ_API_KEY`

**HuggingFace Token** (Optional):
- Only needed if you hit rate limits on embedding models
- Get it from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

## 🔧 Configuration

Create a `.env` file in the root directory with the following variables:

```env
# API Keys (Required)
GROQ_API_KEY=your_groq_api_key_here

# Optional: HuggingFace token (only needed if you hit rate limits)
HUGGINGFACE_API_TOKEN=your_huggingface_token_here
```


**Note**: This is a RAG system for legal document processing. Ensure compliance with all applicable data privacy and legal regulations when processing sensitive documents.