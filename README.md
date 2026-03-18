# AI Resume & Job Description Matcher

## Overview

This project is an AI-powered backend service that evaluates how well a candidate’s resume matches a given job description.

The focus of this implementation was to build a **clean, modular MVP** with strong backend design and practical AI integration, rather than spending time on UI.

The system accepts a resume (PDF) and a job description, and returns:

- Match score (0–100)
- Short explanation
- Missing skills
- Suggestions for improvement

---

## Tech Stack

- Python (FastAPI, asyncio)
- Groq API (LLaMA 3.1 8B)
- PyPDF2 (PDF parsing)
- pytesseract + Pillow (OCR for scanned PDFs)
- Logging for debugging

---

## System Design & Architecture

The project follows a modular, service-oriented structure:

- **Controller Layer**
  - Handles HTTP requests asynchronously
  - Validates inputs and handles structured errors
- **Service Layer**
  - `parser`: Extracts text from PDF with OCR fallback
  - `ai`: Async LLM interaction with Groq
  - `match`: Core business logic for evaluation
- **Model Layer**
  - Structures and validates AI response

An abstraction (`BaseAIService`) decouples the AI provider, allowing easy replacement of Groq with other LLMs like OpenAI.

---

## How It Works

1. User uploads a resume (PDF) and provides a job description.
2. The parser extracts text from the resume. If the PDF is scanned, OCR is applied.
3. A structured prompt is generated and sent to the AI model.
4. The AI evaluates:
   - Skill match
   - Experience alignment
   - Missing skills
5. The response is cleaned, validated, and returned as structured JSON.
6. Rule-based fallback logic adjusts the score based on missing skills and ensures score is between 0–100.

---

## AI Design Decisions

### Why Groq?

- Free tier available for testing
- Fast response times
- Sufficient quality for MVP use case

### Prompt Strategy

- Enforces strict JSON output
- Score constrained between 0–100
- Provides short, precise explanation
- Reduces hallucination and ensures consistent structure

---

## Reliability Improvements

Since LLM outputs can be non-deterministic, safeguards were implemented:

- Input validation (empty resume / job description)
- JSON parsing with fallback handling
- Type validation for AI response
- Score sanity checks (0–100 clamp)
- Rule-based adjustments based on missing skills
- OCR fallback for scanned PDFs
- Logging at each step for debugging

---

## Limitations

- Scoring depends on LLM reasoning (non-deterministic)
- Semantic similarity using embeddings not implemented
- OCR may produce imperfect text for scanned PDFs
- No persistence layer — results are not stored

---

## Future Improvements

- Add embedding-based similarity for better accuracy
- Hybrid scoring (LLM + rule-based / keyword matching)
- Support for DOCX and improved OCR for scanned PDFs
- Store results and compare multiple candidates (rankings)
- Retry logic for AI API calls
- Async batch processing for scalability

---

## Example Output

```json
{
  "score": 78,
  "explanation": "Strong backend experience but lacks cloud skills",
  "missing_skills": ["AWS", "Docker"],
  "suggestions": ["Include cloud projects", "Highlight containerization experience"]
} 
```

## Project Structure

│   .env
│   config.py
│   main.py
│   redme.md
│   requirement.txt
|   logger.py
├───controller
│   │   match_controller.py
├───models
│   │   response_model.py
├───service
│   ├───ai
│   │   │   base_ai.py
│   │   │   groq_service.py
│   ├───match
│   │   │   resume_matcher.py
│   └───parser
│       │   pdf_parser.py
