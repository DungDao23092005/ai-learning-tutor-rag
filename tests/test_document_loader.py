from io import BytesIO

import pytest
from pypdf import PdfWriter

from src.document_loader import clean_text, get_document_stats, load_pdf_pages


def make_sample_pdf(text: str = "Hello World") -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(612, 792)
    writer.pages[0].merge_page(writer.add_blank_page(612, 792))
    buf = BytesIO()
    writer.write(buf)
    buf.seek(0)
    return buf.read()


class TestCleanText:

    def test_removes_empty_lines(self):
        result = clean_text("  Hello  \n  \n  World  ")
        assert result == "Hello\nWorld"

    def test_handles_empty_input(self):
        assert clean_text("") == ""

    def test_preserves_single_line(self):
        assert clean_text("Hello World") == "Hello World"

    def test_strips_whitespace(self):
        result = clean_text("  Line one  \n  Line two  ")
        assert result == "Line one\nLine two"


class TestLoadPdfPages:

    def test_returns_list(self):
        pages = load_pdf_pages(make_sample_pdf())
        assert isinstance(pages, list)

    def test_each_page_has_required_keys(self):
        pages = load_pdf_pages(make_sample_pdf())
        for page in pages:
            assert "page_number" in page
            assert "text" in page

    def test_page_numbers_are_one_indexed(self):
        pages = load_pdf_pages(make_sample_pdf())
        assert pages[0]["page_number"] == 1


class TestGetDocumentStats:

    def test_returns_correct_counts(self):
        pages = [
            {"page_number": 1, "text": "Hello world"},
            {"page_number": 2, "text": "Foo bar baz"},
        ]
        stats = get_document_stats(pages)
        assert stats["total_pages"] == 2
        assert stats["pages_with_text"] == 2
        assert stats["total_words"] == 5

    def test_counts_empty_pages_correctly(self):
        pages = [
            {"page_number": 1, "text": "Hello"},
            {"page_number": 2, "text": ""},
        ]
        stats = get_document_stats(pages)
        assert stats["total_pages"] == 2
        assert stats["pages_with_text"] == 1
