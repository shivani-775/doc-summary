import json
import os
import re

from google import genai
from google.genai import types


_client = None


def client():
    """
    Create and cache the Gemini client.
    """
    global _client

    if _client is None:
        key = os.getenv("GEMINI_API_KEY")

        if not key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        _client = genai.Client(api_key=key)

    return _client


def model_name():
    """
    Gemini model used by the application.

    Gemini 3.5 Flash-Lite is currently a stable,
    low-cost model suitable for document parsing
    and high-throughput applications.
    """
    return os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite"
    )


def ask(prompt: str):
    """
    Send a prompt to Gemini and return the text response.
    """

    response = client().models.generate_content(
        model=model_name(),
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=2500,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "The AI service returned an empty response."
        )

    return response.text.strip()


def parse_json(text: str):
    """
    Extract JSON from the model response.

    Gemini may occasionally wrap JSON in markdown
    code fences, so we remove those before parsing.
    """

    text = text.strip()

    # Remove markdown code fences if present
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        # Try to find the JSON object inside additional text
        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if not match:
            raise ValueError(
                "AI response was not valid JSON."
            )

        try:
            return json.loads(match.group(0))

        except json.JSONDecodeError as exc:
            raise ValueError(
                "AI response contained invalid JSON."
            ) from exc


def generate_summary(pages, length):
    """
    Generate a document summary, key points,
    and improvement suggestions.
    """

    document = "\n\n".join(
        f"[Page {page['page']}]\n{page['text']}"
        for page in pages
    )

    limits = {
        "small": "3-5 sentences",
        "medium": "1-2 detailed paragraphs",
        "large": "4-7 detailed paragraphs",
    }

    target = limits.get(
        length,
        limits["medium"]
    )

    prompt = f"""
You are DocuMind, an AI document analysis assistant.

Your task is to analyze the supplied document.

IMPORTANT RULES:

1. Use ONLY information contained in the document.
2. Do not invent facts.
3. Do not make assumptions that are not supported by the document.
4. Preserve important dates, names, numbers, decisions,
   responsibilities, deadlines, and actions.
5. If information is missing, do not fabricate it.
6. Return ONLY valid JSON.
7. Do not use markdown code fences.

Return exactly this JSON structure:

{{
    "summary": "string",
    "key_points": [
        "string",
        "string"
    ],
    "improvements": [
        "string",
        "string"
    ]
}}

SUMMARY LENGTH:
The summary should be approximately {target}.

KEY POINTS:
Include the most important facts, dates, names,
decisions, responsibilities, deadlines, and actions.

IMPROVEMENTS:
Suggest useful ways the document could be clearer,
more complete, or better structured.

Do NOT invent missing information.

DOCUMENT:

{document}
"""

    result = parse_json(
        ask(prompt)
    )

    # Basic validation
    if not isinstance(result, dict):
        raise ValueError(
            "AI returned an invalid summary structure."
        )

    result.setdefault("summary", "")
    result.setdefault("key_points", [])
    result.setdefault("improvements", [])

    if not isinstance(result["summary"], str):
        result["summary"] = str(result["summary"])

    if not isinstance(result["key_points"], list):
        result["key_points"] = []

    if not isinstance(result["improvements"], list):
        result["improvements"] = []

    return result


def answer_question(chunks, question):
    """
    Answer a user's question using only relevant
    document chunks.
    """

    context = "\n\n".join(
        f"[Page {chunk['page']}]\n{chunk['text']}"
        for chunk in chunks
    )

    prompt = f"""
You are DocuMind, an AI assistant that answers
questions about an uploaded document.

IMPORTANT RULES:

1. Answer ONLY using the document context provided below.
2. Never use outside knowledge to answer the question.
3. Never guess.
4. If the answer is not present in the document,
   clearly say that the document does not provide
   that information.
5. Preserve exact dates, names, numbers, and facts.
6. Return ONLY valid JSON.
7. Do not use markdown code fences.

Return exactly:

{{
    "answer": "string",
    "sources": [1, 2]
}}

The "sources" array must contain the page numbers
that support your answer.

If multiple pages support the answer, include all
relevant page numbers.

If the answer cannot be found, return an answer
explaining that the document does not provide the
requested information and use an empty sources array.

QUESTION:

{question}

DOCUMENT CONTEXT:

{context}
"""

    result = parse_json(
        ask(prompt)
    )

    if not isinstance(result, dict):
        raise ValueError(
            "AI returned an invalid answer structure."
        )

    answer = result.get(
        "answer",
        "The document does not provide that information."
    )

    sources = result.get(
        "sources",
        []
    )

    if not isinstance(sources, list):
        sources = []

    # Only allow pages that were actually provided
    valid_pages = sorted({
        chunk["page"]
        for chunk in chunks
    })

    cleaned_sources = []

    for page in sources:
        try:
            page_number = int(page)

            if page_number in valid_pages:
                cleaned_sources.append(page_number)

        except (ValueError, TypeError):
            continue

    result["answer"] = str(answer)
    result["sources"] = sorted(
        set(cleaned_sources)
    )

    return result