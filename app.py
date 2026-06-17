import streamlit as st


# =========================
# Page configuration
# =========================
st.set_page_config(
    page_title="AI Learning Tutor RAG",
    page_icon="📚",
    layout="wide"
)


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
        "Current stage: UI prototype. "
        "PDF processing and RAG features will be added in the next commits."
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
    st.success(f"Uploaded file: {uploaded_file.name}")
else:
    st.warning("Please upload a PDF file to start.")


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