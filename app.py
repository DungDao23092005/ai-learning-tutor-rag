import streamlit as st

from src.document_loader import get_document_stats, load_pdf_pages


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

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None


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
        "Current stage: PDF upload and text extraction. "
        "RAG features will be added in the next commits."
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

    # Only process again when a new file is uploaded
    if st.session_state.uploaded_file_name != uploaded_file.name:
        with st.spinner("Reading PDF file..."):
            pages = load_pdf_pages(file_bytes)
            stats = get_document_stats(pages)

            st.session_state.pdf_pages = pages
            st.session_state.pdf_stats = stats
            st.session_state.uploaded_file_name = uploaded_file.name

    st.success(f"Uploaded file: {uploaded_file.name}")

    stats = st.session_state.pdf_stats

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total pages", stats["total_pages"])
    col2.metric("Pages with text", stats["pages_with_text"])
    col3.metric("Words", stats["total_words"])
    col4.metric("Characters", stats["total_characters"])

    if stats["pages_with_text"] == 0:
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
# Tabs
# =========================
chat_tab, summary_tab, quiz_tab = st.tabs(
    ["💬 Chat with PDF", "📝 Summary", "❓ Quiz"]
)


# =========================
# Chat tab
# =========================
with chat_tab:
    st.subheader("Ask questions from your PDF")

    user_question = st.text_input(
        "Your question",
        placeholder="Example: What is Linear Regression?"
    )

    ask_button = st.button("Ask", type="primary")

    if ask_button:
        if uploaded_file is None:
            st.error("Please upload a PDF first.")
        elif not user_question.strip():
            st.error("Please enter a question.")
        else:
            st.info("RAG answer will be generated here in a later commit.")

    st.markdown("### Answer")
    st.write("The answer will appear here.")

    st.markdown("### Sources")
    st.write("Relevant source chunks and page numbers will appear here.")


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