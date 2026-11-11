# FLOUNA - AI-Powered Food Decision Engine

## Overview
A full-stack application that processes natural language queries to recommend food options from multiple mock providers. 

## Technology Stack
- **Frontend**: React, Vite, standard CSS.
- **Backend**: Python Flask, scikit-learn.
- **Testing**: pytest.

## Architecture
- **NLP/ML**: Uses Rule-based regex for strict constraints (budget, rating, time) and TF-IDF with Cosine Similarity for relevance matching.
- **Data Normalization**: Handles 3 disparate JSON provider formats and merges duplicate entries, retaining highest-rated options.

## Run Instructions

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest tests/
python app.py
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

## AI Tools Disclosure
Assisted by Gemini for structural generation and scikit-learn boilerplate.
