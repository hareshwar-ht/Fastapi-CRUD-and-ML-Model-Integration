# Insurance Premium Prediction System

A simple machine learning integration project featuring a FastAPI backend for model inference and a Streamlit frontend for user interaction.

## Project Structure

- **`backend/`**: FastAPI application that serves the ML model via a `/predict` endpoint.
- **`frontend/`**: Streamlit application providing a user interface for inputting data and viewing predictions.
- **`docker-compose.yml`**: Configuration for running both services in Docker containers.

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)

### Running with Docker (Recommended)

To spin up both the backend and frontend services:

```bash
docker compose up --build
```

- **Backend**: Accessible at `http://localhost:8005`
- **Frontend**: Accessible at `http://localhost:8501`

### Running Locally

#### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8005
```

#### 2. Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run frontend_streamlit.py
```

_(Ensure the `AI_URL` in `frontend/.env` points to the running backend)_

## Features

- Input user details like Age, BMI (calculated from Height/Weight), Income, etc.
- Real-time insurance premium category prediction.
- Fully containerized for easy deployment.
