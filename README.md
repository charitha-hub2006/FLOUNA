# FLOUNA – AI-Powered Food Discovery and Recommendation System

## 1. Problem Statement
Finding suitable food options can be difficult when users have specific preferences regarding food type, budget, preparation time, and ratings.

FLOUNA aims to simplify food discovery by extracting user preferences from natural-language requests and recommending relevant food options.

## 2. Project Approach
The application follows these steps:

1. Accepts a natural-language food request.
2. Extracts preferences such as food item, dietary preference, budget, time, and rating preference.
3. Processes and normalizes food information from the available data providers.
4. Removes duplicate results.
5. Uses similarity-based ranking to identify relevant recommendations.
6. Displays recommendations through the frontend.

## 3. Architecture
Explain the frontend, backend, NLP/ML module, recommendation engine, and data sources.

Refer to the architecture PDF available in the `docs/` folder.

## 4. Technologies Used
- Frontend: [Enter actual technologies]
- Backend: Python, Flask [if used]
- NLP/ML: Scikit-learn
- Ranking: TF-IDF and Cosine Similarity
- Database: [Enter if used]

## 5. AI/ML Component and Selection
FLOUNA uses TF-IDF vectorization and cosine similarity for text-based preference matching.

**Why selected?**
- TF-IDF converts text into numerical representations.
- Cosine similarity measures similarity between user preferences and food descriptions.
- These techniques are lightweight and suitable for a small-scale recommendation system.

This approach does not require training a large language model.

## 6. Setup and Execution
Add the exact installation and execution commands for the backend and frontend.

## 7. APIs, Mock APIs and Datasets
List all actual data providers, API endpoints, mock data sources, and datasets used.

If no public dataset or external API was used, explicitly mention that.

## 8. Sample Input and Output

**Input:**
Find vegetarian biryani under ₹300 within 30 minutes. I prefer highly rated restaurants.

**Expected preference extraction:**
- Intent: Discovery
- Food item: Biryani
- Dietary preference: Vegetarian
- Maximum budget: ₹300
- Maximum time: 30 minutes
- Rating preference: High

Include your actual application output and screenshots.

## 9. Testing and Edge Cases
Include:
- Test cases for preference extraction.
- Missing or incomplete user preferences.
- No matching recommendations.
- Duplicate food entries.
- Invalid or empty input.

Include actual test results and screenshots or logs.

## 10. Limitations and Future Improvements
Mention actual limitations, such as:
- Limited availability of real-time food data, if applicable.
- Dependence on the quality of available food information.
- Improvements to recommendation accuracy.
- Integration with additional live food providers.

## 11. Demo
[Insert your screen-recording link]

## 12. Libraries, APIs, Datasets and AI Tools
List the actual libraries, APIs, datasets, and AI tools used, with their purposes.

## 13. Author
Charitha
