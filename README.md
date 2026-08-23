# DocuMind — Document Intelligence Assistant

> AI-powered document summarization and Q&A for PDF and image documents.

## 🚀 Live Demo

**[Open DocuMind](https://doc-summary-1h5chr1ro-shivani-973a.vercel.app/)**

## 📦 GitHub Repository

**[View Source Code](https://github.com/shivani-775/doc-summary)**

---

## Overview

DocuMind is a web application that accepts PDF and image documents, extracts their text, generates configurable AI summaries, identifies key points and improvement suggestions, and allows users to ask grounded questions about the uploaded document.

The application is designed to make long or scanned documents easier to understand and interact with.

---

## Features

- 📄 PDF document upload
- 🖼️ Image document upload
- 🖱️ Drag-and-drop and file picker support
- 🔍 PDF text extraction using PyMuPDF
- 👁️ OCR for scanned PDFs and images using Tesseract
- 📝 Short, Medium, and Long AI summaries
- 📌 Key points and main ideas
- 💡 Improvement suggestions
- 💬 AI-powered document Q&A
- 📑 Page references for Q&A answers
- 📱 Desktop / Phone preview toggle
- ⏳ Loading states
- ⚠️ Error handling
- 📱 Responsive UI

---

## Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ React + TypeScript  │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │    PyMuPDF      │        │    Tesseract    │
        │  Digital PDFs   │        │   OCR / Scans   │
        └────────┬────────┘        └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Extracted Text    │
                    │   + Page Numbers    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Gemini API       │
                    │  Summary + Q&A      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Results displayed   │
                    │      to user        │
                    └─────────────────────┘
