from pathlib import Path
import io
import re

import fitz
import pytesseract
from PIL import Image


# Tell pytesseract exactly where Tesseract OCR is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

ALLOWED = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf(data: bytes):
    doc = fitz.open(stream=data, filetype="pdf")
    pages = []

    for i, page in enumerate(doc):
        # First try normal PDF text extraction
        text = clean_text(page.get_text("text"))

        if text:
            pages.append({
                "page": i + 1,
                "text": text
            })

        else:
            # If the PDF page contains no selectable text,
            # render it as an image and use OCR.
            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2),
                alpha=False
            )

            image = Image.open(
                io.BytesIO(pix.tobytes("png"))
            )

            ocr = clean_text(
                pytesseract.image_to_string(image)
            )

            if ocr:
                pages.append({
                    "page": i + 1,
                    "text": ocr
                })

    doc.close()
    return pages


def extract_image(data: bytes):
    image = Image.open(io.BytesIO(data))

    text = clean_text(
        pytesseract.image_to_string(image)
    )

    return [{"page": 1, "text": text}] if text else []


def extract_document(filename: str, data: bytes):
    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED:
        raise ValueError(
            "Unsupported file type. "
            "Upload a PDF, PNG, JPG, JPEG, or WEBP file."
        )

    if ext == ".pdf":
        pages = extract_pdf(data)
    else:
        pages = extract_image(data)

    if not pages:
        raise ValueError(
            "No readable text was found. "
            "Try a clearer scan or another document."
        )

    return pages