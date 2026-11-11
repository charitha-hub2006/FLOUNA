# FLOUNA – AI-Powered Food Decision Engine

## 1. Problem Statement

Finding suitable food options can be difficult when users have multiple preferences, such as food type, cuisine, budget, delivery time, and restaurant ratings.

Traditional food discovery often requires users to manually compare multiple options.

FLOUNA is an AI-assisted food discovery and recommendation application that accepts natural-language food requests, extracts user preferences, compares food options from multiple mock data providers, and recommends suitable restaurants with explanations.

## 2. Project Approach

FLOUNA follows a hybrid NLP and recommendation approach.

The application works through these steps:

1. The user enters a natural-language food request.
2. The backend extracts relevant preferences using rule-based NLP and regular expressions.
3. Restaurant information is loaded from three mock JSON data providers.
4. Data from different providers is converted into a common format.
5. Duplicate restaurant records are identified and handled.
6. Budget, delivery time, and rating constraints are applied.
7. Scikit-learn TF-IDF and cosine similarity are used to calculate menu relevance.
8. A combined score based on text similarity and restaurant rating is calculated.
9. The application displays ranked recommendations and explanations.

## 3. System Architecture

### Frontend
- React – builds the user interface.
- Vite – frontend development server and build tool.
- Tailwind CSS – interface styling.
- Browser localStorage – stores search history.

### Backend
- Python – backend programming language.
- Flask – provides the backend REST API.
- Flask-CORS – enables communication between the frontend and backend.

### Backend Modules

| Module | Responsibility |
|---|---|
| `app.py` | Flask application, API routing, and provider data loading |
| `nlp.py` | Extracts user preferences using regex-based NLP |
| `normalizer.py` | Converts different provider formats into a common structure and removes duplicates |
| `recommendation.py` | Applies constraints, TF-IDF, cosine similarity, and recommendation ranking |
| `data/` | Contains the three mock JSON provider datasets |
| `tests/` | Contains automated backend tests |

### Data Flow

User Request → React Frontend → Flask API → NLP Preference Extraction → Mock Data Providers → Data Normalization → Deduplication → Filtering and Ranking → Recommendation Explanation → Frontend Results

The complete architecture diagram is available in `docs/FLOUNA_Architecture.pdf`.

## 4. Technologies Used

| Category | Technology | Purpose |
|---|---|---|
| Programming language | Python | Backend implementation |
| Frontend | React | User interface |
| Frontend tooling | Vite | Development server and build tooling |
| Styling | Tailwind CSS | UI styling |
| Backend framework | Flask | REST API development |
| Cross-origin communication | Flask-CORS | Frontend/backend communication |
| NLP | Python regular expressions (Regex) | Rule-based preference extraction |
| Machine Learning | Scikit-learn | Text vectorization and similarity |
| Text representation | TF-IDF Vectorizer | Converts text into numerical vectors |
| Similarity calculation | Cosine Similarity | Measures text similarity |
| Testing | Pytest | Automated backend testing |
| Browser storage | localStorage | Search history persistence |
| Data format | JSON | Mock provider data |

## 5. AI/ML Component and Why It Was Selected

FLOUNA uses a hybrid approach combining rule-based NLP and content-based recommendation.

### A. Rule-Based NLP

The `backend/nlp.py` module uses regular expressions and predefined patterns to identify information in the user's request.

It extracts preferences such as:
- Intent
- Food item or cuisine
- Dietary preference
- Maximum budget
- Maximum delivery time
- Minimum rating or rating preference

The extracted information is returned in a structured format.

**Why selected?**
- Lightweight and easy to understand.
- Suitable for extracting explicit constraints.
- Avoids inventing preferences that the user did not provide.
- Does not require an external LLM API.

### B. TF-IDF Vectorization

The recommendation module uses Scikit-learn's `TfidfVectorizer`.

TF-IDF converts the user query and restaurant descriptions into numerical vectors.

The restaurant text includes information such as restaurant name, cuisine, and menu items.

### C. Cosine Similarity

Cosine similarity compares the vector representing the user's query with the vectors representing available restaurant options.

A higher similarity score indicates stronger text relevance.

### D. Composite Recommendation Ranking

The system combines text similarity and normalized restaurant rating.

The implemented scoring formula is:

Final Score = (0.5 × Text Similarity + 0.5 × Normalized Rating) × 100

The system applies available budget, delivery-time, and minimum-rating constraints before ranking.

This approach was selected because it is lightweight, explainable, and does not require a large language model or paid cloud inference.

## 6. Data Sources and Normalization

FLOUNA uses three local mock JSON data providers:

- Provider A – `provider_a.json`
- Provider B – `provider_b.json`
- Provider C – `provider_c.json`

These providers represent different restaurant data formats.

The normalizer converts different field names and structures into a common format containing:
- Restaurant name
- Cuisine
- Cost
- Estimated delivery time
- Rating
- Provider name
- Menu items

### Duplicate Handling

Duplicate restaurant names are identified without considering letter case. When duplicates are found, the entry with the higher rating is retained.

### Imperfect Data Handling

The normalizer is designed to handle different provider formats, missing optional fields, and menu items represented as either strings or dictionaries.

No live commercial restaurant API is claimed in this implementation.

## 7. Setup and Execution

### Prerequisites

- Python 3.11
- Node.js and npm
- Git

### Backend Setup

Open a terminal:

```bash
cd backend
```

Create and activate a virtual environment if one does not already exist:

```bash
python3.11 -m venv venv311
source venv311/bin/activate
```

Install the backend dependencies:

```bash
pip install flask flask-cors scikit-learn pytest
```

If the project contains a `requirements.txt`, use it instead:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
python app.py
```

Backend address:

`http://127.0.0.1:5000`

### Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Frontend address:

`http://localhost:5173`

Keep both terminals running while using the application.

## 8. Sample Inputs and Outputs

### Example 1: Normal Food Request

**Input:**

```text
Find vegetarian biryani under ₹300 within 30 minutes.
I prefer highly rated restaurants.
```

**Extracted preferences:**

- Intent: Discovery
- Food item: Biryani
- Dietary preference: Vegetarian
- Maximum budget: ₹300
- Maximum delivery time: 30 minutes
- Rating preference: High

The recommendation engine uses the available data to filter and rank suitable options.

Add an actual screenshot of the application's extracted preferences and recommendation results here.

### Example 2: Incomplete Request

**Input:**

```text
Find some good food.
```

The system should process the available information without inventing missing budget, delivery-time, or rating preferences.

Add the actual output from your running application here.

## 9. Testing and Edge Cases

FLOUNA includes an automated backend test suite using Pytest.

The test suite covers scenarios such as:

- Normal food requests.
- Missing user preferences.
- Duplicate restaurant records.
- Provider errors.
- Recommendation ranking where the cheapest option is not necessarily the best fit.

The implementation also handles heterogeneous provider data and incomplete optional fields in normalization.

### Run Tests

```bash
cd backend
source venv311/bin/activate
pytest -v
```

**Previously observed test result:** 3 tests passed.

Rerun the tests on the final version before submission and update this result if it changes.

Add screenshots of the actual test output here.

## 10. Limitations and Future Improvements

### Current Limitations

- Restaurant information is based on local mock JSON data rather than live restaurant platforms.
- Rule-based NLP may not understand every variation of natural-language requests.
- TF-IDF relies on textual overlap and may not fully understand deeper semantic relationships.
- Recommendation quality depends on the accuracy and completeness of provider data.
- The current system has a limited set of mock providers.

### Future Improvements

- Integrate additional reliable restaurant data providers.
- Improve natural-language understanding for complex requests.
- Add more advanced semantic recommendation techniques.
- Expand automated tests for provider timeouts and incomplete responses.
- Improve recommendation evaluation using a larger test dataset.
- Add more user preference and history-management capabilities.

## 11. Project Demo

**Demo video:** [Insert your Google Drive or YouTube link]

The demonstration should show:
1. Opening the FLOUNA application.
2. Entering a natural-language food request.
3. Displaying extracted preferences.
4. Showing ranked restaurant recommendations.
5. Displaying recommendation explanations.
6. Demonstrating an incomplete or edge-case request.

## 12. Libraries, APIs, Datasets and AI Tools

### Major Libraries

- Flask – backend API.
- Flask-CORS – cross-origin request handling.
- Scikit-learn – TF-IDF and cosine similarity.
- Pytest – automated testing.
- React – frontend UI.
- Vite – frontend development tooling.
- Tailwind CSS – styling.

### APIs

- Flask REST endpoint: `/api/recommend`
- Three local mock JSON data providers.
- No external commercial restaurant API is used in the current implementation.

### Datasets

- `provider_a.json`
- `provider_b.json`
- `provider_c.json`

These are mock datasets used to demonstrate multi-provider data ingestion, normalization, deduplication, and recommendation.

### AI Development Tools

- Google Gemini – used as an AI-assisted development tool for architecture guidance and implementation support.

The running application uses its own regex-based NLP and Scikit-learn recommendation logic; Gemini is not a runtime dependency.

## 13. Author

**Charitha**

Project: FLOUNA – AI-Powered Food Decision Engine

