from typing import Dict, List


def split_text_into_chunks(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:
    """
    Split a long text into smaller overlapping chunks.

    Args:
        text: Input text.
        chunk_size: Maximum number of characters in one chunk.
        chunk_overlap: Number of overlapping characters between chunks.

    Returns:
        A list of text chunks.
    """
    if not text or not text.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # Try to split at a newline first
        if end < text_length:
            newline_break = text.rfind("\n", start, end)
            sentence_break = text.rfind(". ", start, end)

            break_point = max(newline_break, sentence_break)

            # Only use break point if it is not too close to the start
            if break_point > start + chunk_size * 0.5:
                end = break_point + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        next_start = end - chunk_overlap

        # Avoid infinite loop
        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


def split_pages_into_chunks(
    pages: List[Dict],
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Dict]:
    """
    Split PDF pages into chunks while keeping page metadata.

    Args:
        pages: List of page dictionaries from document_loader.py
        chunk_size: Maximum number of characters in one chunk.
        chunk_overlap: Number of overlapping characters between chunks.

    Returns:
        A list of chunk dictionaries.
    """
    all_chunks = []
    global_chunk_id = 1

    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]

        page_chunks = split_text_into_chunks(
            text=page_text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for chunk_index, chunk_text in enumerate(page_chunks, start=1):
            all_chunks.append(
                {
                    "chunk_id": f"chunk-{global_chunk_id}",
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                }
            )

            global_chunk_id += 1

    return all_chunks


def get_chunk_stats(chunks: List[Dict]) -> Dict:
    """
    Calculate simple statistics for chunks.
    """
    if not chunks:
        return {
            "total_chunks": 0,
            "average_chunk_length": 0,
            "min_chunk_length": 0,
            "max_chunk_length": 0,
        }

    chunk_lengths = [len(chunk["text"]) for chunk in chunks]

    return {
        "total_chunks": len(chunks),
        "average_chunk_length": round(sum(chunk_lengths) / len(chunk_lengths), 2),
        "min_chunk_length": min(chunk_lengths),
        "max_chunk_length": max(chunk_lengths),
    }