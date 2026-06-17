# AI Learning Tutor RAG

AI Learning Tutor RAG is a personal AI project that helps users learn from PDF documents.

The app allows users to upload a learning document, ask questions based on the document, summarize the content, generate quizzes, and show source pages used for each answer.

## Main Features

* Upload PDF learning materials
* Ask questions based on uploaded PDF
* Summarize document content
* Generate multiple-choice quizzes
* Show source chunks and page numbers

## Tech Stack

* Python
* Streamlit
* Gemini API
* ChromaDB
* PyPDF

## Project Architecture

```text
User upload PDF
        ↓
Extract text from PDF
        ↓
Split text into chunks
        ↓
Create embeddings
        ↓
Store chunks in vector database
        ↓
User asks a question
        ↓
Retrieve relevant chunks
        ↓
Send context + question to LLM
        ↓
Return answer with sources
```

## Folder Structure

```text
ai-learning-tutor-rag/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── src/
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   ├── rag_chain.py
│   └── quiz_generator.py
│
├── data/
│   └── sample_docs/
│
├── screenshots/
│
└── notebooks/
```

## How to Run

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

On Windows CMD:

```bash
.venv\Scripts\activate
```

On Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```bash
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```bash
copy .env.example .env
```

### 5. Run the app

```bash
streamlit run app.py
```

## Status

This project is under development.
