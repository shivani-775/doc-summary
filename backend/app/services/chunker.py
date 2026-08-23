import re


def make_chunks(pages, words_per_chunk=220):
    chunks = []
    for page in pages:
        words = re.findall(r"\S+", page["text"])
        for start in range(0, len(words), words_per_chunk):
            text = " ".join(words[start:start + words_per_chunk]).strip()
            if text:
                chunks.append({"id": len(chunks), "page": page["page"], "text": text})
    return chunks


def retrieve_chunks(chunks, query, top_k=5):
    terms = {t.lower() for t in re.findall(r"[a-zA-Z0-9]+", query) if len(t) > 2}
    scored = []
    for chunk in chunks:
        words = set(re.findall(r"[a-zA-Z0-9]+", chunk["text"].lower()))
        score = len(terms & words)
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [c for score, c in scored[:top_k] if score > 0]
    return selected or chunks[:top_k]
