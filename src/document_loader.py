from io import BytesIO
from typing import Dict, List

from pypdf import PdfReader


def clean_text(text: str) -> str:
    """
    Clean extracted text from PDF.

    This function removes extra spaces and empty lines
    to make the text easier to process later.
    """
    if not text:
        return ""

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def load_pdf_pages(file_bytes: bytes) -> List[Dict]:
    """
    Extract text from a PDF file.

    Args:
        file_bytes: PDF file content in bytes.

    Returns:
        A list of dictionaries.
        Each dictionary contains:
        - page_number
        - text
    """
    reader = PdfReader(BytesIO(file_bytes))

    pages = []

    for page_index, page in enumerate(reader.pages):
        raw_text = page.extract_text() or ""
        cleaned_text = clean_text(raw_text)

        pages.append(
            {
                "page_number": page_index + 1,
                "text": cleaned_text,
            }
        )

    return pages


def get_document_stats(pages: List[Dict]) -> Dict:
    """
    Calculate simple statistics from extracted PDF pages.
    """
    total_pages = len(pages)
    pages_with_text = sum(1 for page in pages if page["text"].strip())

    all_text = "\n".join(page["text"] for page in pages)
    total_characters = len(all_text)
    total_words = len(all_text.split())

    return {
        "total_pages": total_pages,
        "pages_with_text": pages_with_text,
        "total_characters": total_characters,
        "total_words": total_words,
    }