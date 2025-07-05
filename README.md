
## Deployment

This application is automatically deployed to Google Cloud Run when changes are pushed to the `main` branch. The deployment process is managed by a GitHub Actions workflow defined in `.github/workflows/gcp-deploy.yml`.

The workflow performs the following steps:
1.  **Run Tests:** The Playwright end-to-end tests are run to ensure the application is functioning correctly.
2.  **Build & Push Image:** A Docker image is built and pushed to Google Artifact Registry.
3.  **Deploy to Cloud Run:** The new image is deployed to the Cloud Run service.

The live application can be accessed at the URL provided by the Cloud Run service after the first successful deployment.

# Facebook GPT Integration

This project is a question-and-answer web application about the "Big Beautiful Bill". It uses the OpenAI Assistants API to provide answers from the bill's text.

## Project Status

- **[X] Project Setup**
  - [X] Initialize `git` repository
  - [X] Create GitHub repository
  - [X] Create `README.md`
  - [X] Set up Python virtual environment
  - [X] Install dependencies (`openai`, `fastapi`, `uvicorn`, `python-dotenv`, `playwright`, `pytest-playwright`)
- **[X] OpenAI Assistant Creation**
  - [X] Create Assistant via OpenAI API
  - [X] Store Assistant and Vector Store IDs in `.env`
- **[X] Backend API (FastAPI)**
  - [X] Create `main.py`
  - [X] Implement `/ask` endpoint
  - [X] Serve static frontend
- **[X] Simple Frontend**
  - [X] Create `index.html`
  - [X] Add JavaScript to interact with backend
- **[X] End-to-End Testing (Playwright)**
  - [X] Install Playwright and dependencies
  - [X] Configure `playwright.config.json` for the local server
  - [X] Create `tests/test_e2e.py` with tests for UI and functionality
  - [X] Successfully run all tests

## How to Run

1.  **Install Dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```
2.  **Set up Environment Variables:**
    - Create a `.env` file and add your `OPENAI_API_KEY`, `ASSISTANT_ID`, and `VECTOR_STORE_ID`.
3.  **Start the Application:**
    ```bash
    /Users/noelmcmichael/Workspace/facebook_gpt_integration/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
    ```
4.  **Access the Application:**
    - Open your browser to `http://127.0.0.1:8000`

## How to Run Tests

1.  **Install Test Dependencies:**
    ```bash
    uv pip install playwright pytest-playwright
    /Users/noelmcmichael/Workspace/facebook_gpt_integration/.venv/bin/playwright install
    ```
2.  **Start the Application (if not already running):**
    ```bash
    /Users/noelmcmichael/Workspace/facebook_gpt_integration/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
    ```
3.  **Run the Tests:**
    ```bash
    /Users/noelmcmichael/Workspace/facebook_gpt_integration/.venv/bin/pytest tests/test_e2e.py
    ```
