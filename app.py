import streamlit as st

from src.document_loader import get_document_stats, load_pdf_pages
from src.embedding import create_embedding, create_embeddings_for_chunks, get_embedding_stats
from src.rag_chain import generate_rag_answer
from src.text_splitter import get_chunk_stats, split_pages_into_chunks
from src.vector_store import (
    get_vector_store_stats,
    reset_vector_store,
    search_relevant_chunks,
    store_chunks_in_chroma,
)


# =========================
# Page configuration
# =========================
st.set_page_config(
    page_title="AI Learning Tutor RAG",
    page_icon="📚",
    layout="wide"
)


# =========================
# Session state
# =========================
if "pdf_pages" not in st.session_state:
    st.session_state.pdf_pages = []

if "pdf_stats" not in st.session_state:
    st.session_state.pdf_stats = None

if "text_chunks" not in st.session_state:
    st.session_state.text_chunks = []

if "chunk_stats" not in st.session_state:
    st.session_state.chunk_stats = None

if "embedded_chunks" not in st.session_state:
    st.session_state.embedded_chunks = []

if "embedding_stats" not in st.session_state:
    st.session_state.embedding_stats = None

if "vector_store_stats" not in st.session_state:
    st.session_state.vector_store_stats = None

if "is_vector_store_ready" not in st.session_state:
    st.session_state.is_vector_store_ready = False

if "retrieved_chunks" not in st.session_state:
    st.session_state.retrieved_chunks = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "rag_answer" not in st.session_state:
    st.session_state.rag_answer = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================
# Sidebar
# =========================
with st.sidebar:
    st.title("📚 AI Tutor RAG")

    st.markdown(
        """
        This app helps you learn from your own PDF documents.

        **Main features:**
        - Upload PDF learning materials
        - Ask questions based on the document
        - Summarize document content
        - Generate quiz questions
        - Show source pages
        """
    )

    st.divider()

    st.info(
        "Current stage: RAG chatbot with chat history and source display. "
        "Summary and quiz features will be added in the next commits."
    )

    st.markdown("### Chunk settings")

    chunk_size = st.slider(
        "Chunk size",
        min_value=500,
        max_value=2000,
        value=1000,
        step=100
    )

    chunk_overlap = st.slider(
        "Chunk overlap",
        min_value=50,
        max_value=500,
        value=200,
        step=50
    )


# =========================
# Main title
# =========================
st.title("AI Learning Tutor RAG")
st.write(
    "Upload a learning PDF and ask questions based on its content."
)


# =========================
# Upload section
# =========================
uploaded_file = st.file_uploader(
    label="Upload your PDF document",
    type=["pdf"],
    help="Upload a PDF file such as Machine Learning notes, lecture slides, or textbooks."
)

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()

    if st.session_state.uploaded_file_name != uploaded_file.name:
        st.session_state.embedded_chunks = []
        st.session_state.embedding_stats = None
        st.session_state.vector_store_stats = None
        st.session_state.is_vector_store_ready = False
        st.session_state.retrieved_chunks = []
        st.session_state.rag_answer = ""
        st.session_state.chat_history = []
        reset_vector_store()

    # Process PDF
    with st.spinner("Reading and chunking PDF file..."):
        pages = load_pdf_pages(file_bytes)
        pdf_stats = get_document_stats(pages)

        chunks = split_pages_into_chunks(
            pages=pages,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunk_stats = get_chunk_stats(chunks)

        st.session_state.pdf_pages = pages
        st.session_state.pdf_stats = pdf_stats
        st.session_state.text_chunks = chunks
        st.session_state.chunk_stats = chunk_stats
        st.session_state.uploaded_file_name = uploaded_file.name

    st.success(f"Uploaded file: {uploaded_file.name}")

    pdf_stats = st.session_state.pdf_stats
    chunk_stats = st.session_state.chunk_stats

    st.markdown("### Document statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total pages", pdf_stats["total_pages"])
    col2.metric("Pages with text", pdf_stats["pages_with_text"])
    col3.metric("Words", pdf_stats["total_words"])
    col4.metric("Characters", pdf_stats["total_characters"])

    st.markdown("### Chunk statistics")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Total chunks", chunk_stats["total_chunks"])
    col6.metric("Average length", chunk_stats["average_chunk_length"])
    col7.metric("Min length", chunk_stats["min_chunk_length"])
    col8.metric("Max length", chunk_stats["max_chunk_length"])

    if pdf_stats["pages_with_text"] == 0:
        st.error(
            "No text was extracted from this PDF. "
            "This may be a scanned PDF image. OCR support can be added later."
        )

else:
    st.warning("Please upload a PDF file to start.")


# =========================
# PDF preview
# =========================
if st.session_state.pdf_pages:
    with st.expander("Preview extracted text"):
        selected_page = st.selectbox(
            "Select page",
            options=[
                page["page_number"]
                for page in st.session_state.pdf_pages
            ]
        )

        page_data = next(
            page
            for page in st.session_state.pdf_pages
            if page["page_number"] == selected_page
        )

        preview_text = page_data["text"]

        if preview_text.strip():
            st.text_area(
                label=f"Page {selected_page} text",
                value=preview_text[:3000],
                height=300
            )

            if len(preview_text) > 3000:
                st.caption("Preview is limited to the first 3000 characters.")
        else:
            st.warning("This page has no extractable text.")


# =========================
# Embedding section
# =========================
if st.session_state.text_chunks:
    st.markdown("### Embeddings")

    st.write(
        "Create embeddings for text chunks. "
        "These vectors will be stored in ChromaDB."
    )

    if st.button("Create Embeddings"):
        try:
            with st.spinner("Creating embeddings with Gemini..."):
                embedded_chunks = create_embeddings_for_chunks(
                    st.session_state.text_chunks
                )

                embedding_stats = get_embedding_stats(embedded_chunks)

                st.session_state.embedded_chunks = embedded_chunks
                st.session_state.embedding_stats = embedding_stats

            st.success("Embeddings created successfully.")

        except Exception as error:
            st.error(f"Failed to create embeddings: {error}")

    if st.session_state.embedding_stats:
        col_a, col_b = st.columns(2)

        col_a.metric(
            "Embedded chunks",
            st.session_state.embedding_stats["total_embedded_chunks"]
        )

        col_b.metric(
            "Embedding dimension",
            st.session_state.embedding_stats["embedding_dimension"]
        )

    if st.session_state.embedded_chunks:
        with st.expander("Preview first embedding"):
            first_chunk = st.session_state.embedded_chunks[0]

            st.write(f"**Chunk ID:** {first_chunk['chunk_id']}")
            st.write(f"**Page:** {first_chunk['page_number']}")
            st.write(f"**Vector length:** {len(first_chunk['embedding'])}")

            st.write("First 10 vector values:")

            st.code(first_chunk["embedding"][:10])

    st.markdown("### Vector Database")

    if st.session_state.embedded_chunks:
        if st.button("Store Embeddings in ChromaDB"):
            try:
                with st.spinner("Storing embeddings in ChromaDB..."):
                    reset_vector_store()

                    stored_count = store_chunks_in_chroma(
                        st.session_state.embedded_chunks
                    )

                    vector_store_stats = get_vector_store_stats()

                    st.session_state.vector_store_stats = vector_store_stats
                    st.session_state.is_vector_store_ready = True

                st.success(
                    f"Stored {stored_count} chunks in ChromaDB successfully."
                )

            except Exception as error:
                st.error(f"Failed to store embeddings in ChromaDB: {error}")

    else:
        st.info("Create embeddings first before storing them in ChromaDB.")

    if st.session_state.vector_store_stats:
        col_x, col_y, col_z = st.columns(3)

        col_x.metric(
            "Collection",
            st.session_state.vector_store_stats["collection_name"]
        )

        col_y.metric(
            "Total items",
            st.session_state.vector_store_stats["total_items"]
        )

        col_z.metric(
            "Persist path",
            st.session_state.vector_store_stats["persist_path"]
        )


# =========================
# Chunk preview
# =========================
if st.session_state.text_chunks:
    with st.expander("Preview text chunks"):
        selected_chunk_id = st.selectbox(
            "Select chunk",
            options=[
                chunk["chunk_id"]
                for chunk in st.session_state.text_chunks
            ]
        )

        chunk_data = next(
            chunk
            for chunk in st.session_state.text_chunks
            if chunk["chunk_id"] == selected_chunk_id
        )

        st.write(f"**Chunk ID:** {chunk_data['chunk_id']}")
        st.write(f"**Page:** {chunk_data['page_number']}")
        st.write(f"**Chunk index in page:** {chunk_data['chunk_index']}")

        st.text_area(
            label="Chunk text",
            value=chunk_data["text"],
            height=250
        )


# =========================
# Tabs
# =========================
chat_tab, summary_tab, quiz_tab = st.tabs(
    ["💬 Chat with PDF", "📝 Summary", "❓ Quiz"]
)


# =========================
# Chat tab
# =========================
with chat_tab:
    st.subheader("Chat with your PDF")

    st.caption(
        "Ask questions about the uploaded document. "
        "The assistant will answer using retrieved source chunks."
    )

    col_clear, col_status = st.columns([1, 3])

    with col_clear:
        clear_chat = st.button("Clear chat")

    with col_status:
        if st.session_state.is_vector_store_ready:
            st.success("Vector database is ready. You can ask questions.")
        else:
            st.warning(
                "Please create embeddings and store them in ChromaDB first."
            )

    if clear_chat:
        st.session_state.chat_history = []
        st.session_state.retrieved_chunks = []
        st.session_state.rag_answer = ""
        st.rerun()

    # Display chat history
    if st.session_state.chat_history:
        for chat_item in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat_item["question"])

            with st.chat_message("assistant"):
                st.write(chat_item["answer"])

                with st.expander("View sources"):
                    for index, chunk in enumerate(
                        chat_item["sources"],
                        start=1
                    ):
                        st.markdown(
                            f"**Source {index} — Page {chunk['page_number']}**"
                        )
                        st.caption(
                            f"Chunk ID: {chunk['chunk_id']} | "
                            f"Chunk index: {chunk['chunk_index']} | "
                            f"Distance: {chunk['distance']:.4f}"
                        )
                        st.write(chunk["text"])
                        st.divider()
    else:
        st.info("No chat history yet. Ask your first question below.")

    user_question = st.chat_input(
        "Ask something from your PDF..."
    )

    if user_question:
        if uploaded_file is None:
            st.error("Please upload a PDF first.")
        elif not st.session_state.is_vector_store_ready:
            st.error(
                "Please create embeddings and store them in ChromaDB first."
            )
        else:
            try:
                with st.spinner("Searching relevant chunks..."):
                    query_embedding = create_embedding(
                        text=user_question,
                        task_type="RETRIEVAL_QUERY"
                    )

                    retrieved_chunks = search_relevant_chunks(
                        query_embedding=query_embedding,
                        top_k=3
                    )

                with st.spinner("Generating answer with Gemini..."):
                    rag_answer = generate_rag_answer(
                        question=user_question,
                        retrieved_chunks=retrieved_chunks
                    )

                st.session_state.retrieved_chunks = retrieved_chunks
                st.session_state.rag_answer = rag_answer

                st.session_state.chat_history.append(
                    {
                        "question": user_question,
                        "answer": rag_answer,
                        "sources": retrieved_chunks,
                    }
                )

                st.rerun()

            except Exception as error:
                st.error(f"Failed to generate answer: {error}")

    st.markdown("### Answer")

    if st.session_state.rag_answer:
        st.write(st.session_state.rag_answer)
    else:
        st.write("The answer will appear here after you ask a question.")

    st.markdown("### Sources")

    if st.session_state.retrieved_chunks:
        for index, chunk in enumerate(
            st.session_state.retrieved_chunks,
            start=1
        ):
            with st.expander(
                f"Source {index} | Page {chunk['page_number']} | "
                f"Distance: {chunk['distance']:.4f}"
            ):
                st.write(f"**Chunk ID:** {chunk['chunk_id']}")
                st.write(f"**Page:** {chunk['page_number']}")
                st.write(f"**Chunk index:** {chunk['chunk_index']}")
                st.write(chunk["text"])
    else:
        st.write("Relevant source chunks will appear here.")


# =========================
# Summary tab
# =========================
with summary_tab:
    st.subheader("Summarize document")

    if st.button("Generate Summary"):
        if uploaded_file is None:
            st.error("Please upload a PDF first.")
        else:
            st.info("Document summary will be generated here in a later commit.")

    st.markdown("### Summary")
    st.write("The document summary will appear here.")


# =========================
# Quiz tab
# =========================
with quiz_tab:
    st.subheader("Generate quiz from document")

    number_of_questions = st.slider(
        "Number of questions",
        min_value=3,
        max_value=10,
        value=5
    )

    if st.button("Generate Quiz"):
        if uploaded_file is None:
            st.error("Please upload a PDF first.")
        else:
            st.info(
                f"{number_of_questions} quiz questions will be generated here "
                "in a later commit."
            )

    st.markdown("### Quiz")
    st.write("Generated quiz questions will appear here.")