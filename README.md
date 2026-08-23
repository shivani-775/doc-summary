# DocuMind — Document Intelligence Assistant

DocuMind is a web application that accepts PDF and image documents, extracts their text, generates configurable AI summaries, identifies key points and improvement suggestions, and lets users ask grounded questions about the uploaded document.

## Features
- PDF parsing with PyMuPDF
- OCR fallback for scanned PDF pages and image files using Tesseract
- Short / Medium / Long AI summaries
- Key points and improvement suggestions
- Document Q&A with source page references
- Drag-and-drop upload
- Desktop / Phone preview toggle
- Loading and error states
- Responsive React UI

## Architecture
`React + TypeScript + Tailwind-style CSS` → `FastAPI` → `PyMuPDF/Tesseract` → `Gemini API`

The backend keeps the current document in memory for the active demo session. Text is split into chunks and the most relevant chunks are selected for each question before being sent to the model. This keeps the demo simple without introducing a database or vector-store dependency.

## Prerequisites
- Node.js 20+
- Python 3.11+
- Tesseract OCR installed and available on PATH
- Gemini API key

## Run backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
# Add GEMINI_API_KEY to .env
uvicorn app.main:app --reload --port 8000
```

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

If the backend is deployed separately, create `frontend/.env`:
```env
VITE_API_URL=https://YOUR-BACKEND-DOMAIN/api
```

## Tesseract
Install Tesseract from the official distribution for your operating system and make sure the `tesseract` executable is on PATH. On Windows, if PATH is not available, configure `pytesseract.pytesseract.tesseract_cmd` in `extractor.py`.

## Production notes
For a production deployment, replace the in-memory session store with object storage/database-backed document sessions, add authentication, rate limiting, virus scanning, persistent vector search, and automatic cleanup of uploaded documents.

## 200-word approach
DocuMind is an AI-powered document intelligence assistant designed to turn PDFs and scanned images into actionable information. The application first validates the uploaded file and extracts text using PyMuPDF for digital PDFs. If a PDF page contains little or no extractable text, the page is rendered and passed through Tesseract OCR; image uploads are handled directly by OCR. The extracted content is preserved with page numbers and divided into manageable chunks.

Users can select a short, medium, or long summary. The backend sends the document text to a Gemini model with a structured prompt and returns a summary, key points, and improvement suggestions. For document Q&A, the application scores document chunks against the user's question, selects the most relevant context, and asks the model to answer only from that context. Page references are returned with answers to make responses easier to verify.

The frontend is built with React and TypeScript and includes drag-and-drop upload, clear processing states, error handling, responsive layouts, and a desktop/phone preview toggle. The application can be deployed with the frontend on Vercel and the FastAPI backend on a service such as Render.
