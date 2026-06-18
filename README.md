# AI Learning Tutor RAG

AI Learning Tutor RAG is a personal AI project that helps students learn from their own PDF documents using Retrieval-Augmented Generation.

Users can upload a learning PDF, ask questions about the document, generate summaries, create multiple-choice quizzes, and view the source pages used by the assistant.

This project was built as a portfolio project for AI Engineer / Machine Learning Engineer internship applications.

## Demo Features

* Upload PDF learning materials
* Extract text from PDF pages
* Split document text into page-aware chunks
* Create embeddings for document chunks using Gemini
* Store and search embeddings with ChromaDB
* Ask questions based on uploaded PDF content
* Generate source-grounded RAG answers
* Display source chunks and page numbers
* Generate document summaries
* Generate multiple-choice quizzes
* Check quiz answers and explain mistakes
* Store chat history in the app session

## Tech Stack

* Python
* Streamlit
* Gemini API
* ChromaDB
* PyPDF
* python-dotenv

## Project Architecture

```text
User uploads PDF
        ↓
Extract text from PDF pages
        ↓
Split text into chunks
        ↓
Create embeddings for chunks
        ↓
Store embeddings in ChromaDB
        ↓
User asks a question
        ↓
Create embedding for the question
        ↓
Retrieve relevant chunks from ChromaDB
        ↓
Send context + question to Gemini
        ↓
Generate answer based on document context
        ↓
Display answer with source pages
```

## Folder Structure

```text
ai-learning-tutor-rag/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── rag_chain.py
│   └── quiz_generator.py
│
├── data/
│   └── sample_docs/
│
├── screenshots/
│
├── notebooks/
│
└── .streamlit/
    └── config.toml
```

## Main Modules

### `document_loader.py`

Reads PDF files and extracts text page by page.

### `text_splitter.py`

Splits extracted PDF text into smaller overlapping chunks while keeping page metadata.

### `embedding.py`

Creates Gemini embeddings for document chunks and user questions.

### `vector_store.py`

Stores embeddings in ChromaDB and retrieves relevant chunks for a user query.

### `rag_chain.py`

Builds RAG prompts and generates source-grounded answers using Gemini.

### `quiz_generator.py`

Generates multiple-choice quizzes from document chunks and checks user answers.

### `app.py`

Streamlit web app that connects all modules into an interactive user interface.

## Installation

Clone the repository:

```bash
git clone https://github.com/DungDao23092005/ai-learning-tutor-rag.git
cd ai-learning-tutor-rag
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
copy .env.example .env
```

Add your Gemini API key to `.env`:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Run the app:

```bash
streamlit run app.py
```

## How to Use

1. Upload a PDF learning document.
2. Wait for the app to extract and chunk the document.
3. Click **Create Embeddings**.
4. Click **Store Embeddings in ChromaDB**.
5. Open the **Chat with PDF** tab.
6. Ask questions about the uploaded document.
7. View the generated answer and source chunks.
8. Use the **Summary** tab to summarize the document.
9. Use the **Quiz** tab to generate and answer multiple-choice questions.

## Example Questions

```text
SQL là gì?
Linear Regression là gì?
Overfitting là gì?
Cho tôi ví dụ đơn giản về nội dung này.
Tóm tắt tài liệu này cho tôi.
Tạo 5 câu trắc nghiệm từ tài liệu này.
```

## Screenshots

Add screenshots to the `screenshots/` folder:

```text
screenshots/
├── upload_pdf.png
├── chat_answer.png
├── source_display.png
├── summary.png
└── quiz_generation.png
```

Suggested screenshots:

1. PDF upload and document statistics
2. Chat answer with source pages
3. Source chunk display
4. Document summary
5. Quiz generation and score result

## Commit History Plan

This project was developed step by step with meaningful Git commits:

```text
1. chore: initialize AI tutor RAG project structure
2. feat: build basic Streamlit user interface
3. feat: add PDF upload and text extraction
4. feat: split PDF text into page-aware chunks
5. feat: create Gemini embeddings for text chunks
6. feat: store embeddings in ChromaDB and search chunks
7. feat: generate source-grounded RAG answers
8. feat: add chat history and improved source display
9. feat: add document summary and quiz generation
10. docs: polish README and project documentation
```

## Current Limitations

* Works best with text-based PDFs.
* Scanned image PDFs may not work because OCR is not implemented yet.
* Very large PDFs may take longer to process.
* Quiz generation depends on the quality of extracted document text.
* The current app stores data locally in ChromaDB.

## Future Improvements

* Add OCR support for scanned PDFs
* Add support for DOCX and PPTX files
* Add user authentication
* Add database storage for chat history
* Add better quiz export
* Add Docker support
* Deploy the app to Streamlit Community Cloud or Hugging Face Spaces

## What I Learned

Through this project, I practiced:

* Building an end-to-end RAG pipeline
* PDF text extraction
* Text chunking strategy
* Embedding generation
* Vector database search
* Prompt engineering
* Gemini API integration
* Streamlit app development
* Source-grounded answer generation
* Git workflow with meaningful commits

## License

This project is for learning and portfolio purposes.
