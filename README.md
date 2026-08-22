# LLM Backend Service

A FastAPI-based backend service that provides access to a Large Language Model through the Groq API, with a Streamlit chat interface.

## Features

* FastAPI backend
* Groq API integration
* LLM chat completion
* Streaming responses
* Conversation history
* Configurable system prompt
* Configurable model
* Temperature control
* Maximum token control
* Health check endpoint
* Available models endpoint
* Streamlit frontend
* Automated API tests
* Environment variable configuration

## Project Structure

```text
LLM-Backend-Service/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py
│   │       ├── health.py
│   │       └── models.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── schemas/
│   │   └── chat.py
│   │
│   ├── services/
│   │   └── llm_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_chat.py
│   ├── test_health.py
│   └── test_models.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── streamlit_app.py
```

## Technologies

* Python
* FastAPI
* Uvicorn
* Groq API
* Streamlit
* Pydantic
* Requests
* Pytest

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add the Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit the actual API key to GitHub or share it publicly.

## Run the Backend

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Run the Streamlit Frontend

In a second terminal:

```powershell
streamlit run streamlit_app.py
```

The Streamlit interface will open in the browser.

## API Endpoints

### Health Check

```text
GET /health
```

Checks whether the backend service is running.

### Models

```text
GET /models
```

Returns the available LLM models.

### Chat

```text
POST /chat
```

Sends a message to the LLM and returns the generated response.

### Streaming Chat

```text
POST /chat/stream
```

Returns the LLM response progressively as it is generated.

## Testing

Run all tests with:

```powershell
pytest
```

Run a specific test file:

```powershell
pytest tests/test_chat.py
```

## Project Goal

The goal of this project is to develop a clean and modular backend service for interacting with an LLM. FastAPI provides the backend API, Groq provides the LLM inference service, and Streamlit provides a simple user interface for interacting with the model.
