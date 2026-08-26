#  Medical Appointment System

An AI-powered medical appointment management application that combines appointment scheduling with an intelligent healthcare assistant. The application provides a modern interface for managing patient appointments while leveraging Retrieval-Augmented Generation (RAG) to answer medical-related questions using a semantic knowledge base.

---

##  Overview

The Medical Appointment Assistant is a full-stack healthcare application designed to simplify appointment management while providing users with AI-assisted medical information. The backend is built using FastAPI, the frontend uses Streamlit, and PostgreSQL is used for persistent data storage. ChromaDB is integrated to cache AI responses and improve response times for repeated queries.

This project demonstrates modern software engineering practices including RESTful API development, authentication, containerization with Docker, database integration, and AI-powered semantic search.

---

##  Features

### Appointment Management

* Create new appointments
* View scheduled appointments
* Store appointment information in PostgreSQL
* RESTful API architecture

### AI Medical Assistant

* AI-powered healthcare question answering
* Semantic similarity search using ChromaDB
* Response caching to improve performance
* Retrieval-Augmented Generation (RAG) workflow

### Authentication

* User authentication
* Secure API endpoints
* Authorization support

### User Interface

* Interactive Streamlit web application
* Easy-to-use appointment management interface
* AI chatbot integration

### Containerized Deployment

* Docker support for frontend and backend
* Easy local deployment
* Consistent development environment

---

##  Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* PostgreSQL

### Frontend

* Streamlit

### AI & Data

* ChromaDB
* Vector similarity search

### DevOps

* Docker
* Docker Compose

---

## Project Structure

medical-appointment-system/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── ai_service.py
│   ├── agent_service.py
│   ├── chroma_cache.py
│   ├── assistant_tools.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── .gitignore
├── README.md
└── docker-compose.yml

## AI Workflow

The AI assistant follows a retrieval and caching workflow:

User Question
      │
      ▼
Check ChromaDB Cache
      │
      ├── Cached Response Found
      │          │
      │          ▼
      │      Return Response
      │
      └── No Cached Response
                 │
                 ▼
          Generate AI Response
                 │
                 ▼
          Store in ChromaDB
                 │
                 ▼
            Return Response

This approach demonstrates how semantic retrieval and response caching can be incorporated into an AI-enabled application.

## API Endpoints

The application exposes RESTful endpoints for core functionality.

Examples include:

POST /appointments
GET  /appointments
POST /login
POST /chat

The FastAPI application also provides interactive API documentation through Swagger UI when running locally.

http://localhost:8000/docs

## Local Development

# Prerequisites

Make sure you have:

Python 3.10+
PostgreSQL
Docker Desktop
Git

# 1. Clone the repository
git clone https://github.com/juliagrace07/medical-appointment-system.git
cd medical-appointment-system

# 2. Backend setup
cd backend
python -m venv venv
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start the backend:

uvicorn main:app --reload

The API will be available at:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

# 3. Frontend setup

Open a new terminal:

cd frontend
pip install -r requirements.txt

Start Streamlit:

streamlit run app.py

## Docker

The application can also be run using Docker Compose.

From the project root:

docker compose up --build

To stop the containers:

docker compose down

## Environment Variables

Create a local .env file for environment-specific configuration.

Never commit API keys, passwords, or other secrets to GitHub.

A public .env.example file will be provided to document the required configuration without exposing credentials.

## Application Screenshots

Application Dashboard




Appointment Management




AI Assistant




API Documentation




## Testing

Automated tests are being added to validate core application functionality, API behavior, and appointment-management workflows.

Test suite:

pytest

## Future Improvements

Doctor availability management
Email and SMS appointment reminders
Expanded role-based access control
Calendar integration
Analytics dashboard
Cloud deployment
Expanded automated test coverage
Improved AI retrieval and evaluation
Production monitoring

## What This Project Demonstrates

This project demonstrates practical experience with:

REST API development
FastAPI backend architecture
Database modeling
PostgreSQL integration
Authentication
Full-stack application development
Docker containerization
Vector search
Retrieval-Augmented Generation
AI response caching
API documentation
Software architecture

##  Author

**Julia Grace Muddada**

* GitHub: https://github.com/juliagrace07
* LinkedIn: https://www.linkedin.com/in/julia-grace-muddada-6708271b3
