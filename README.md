# Medical Appointment System

A full-stack healthcare application that combines medical appointment management with an AI-assisted healthcare information interface. The application uses FastAPI for the backend, Streamlit for the frontend, PostgreSQL for persistent data storage, and ChromaDB for vector-based retrieval and response caching.

> **Disclaimer:** This project is intended for educational and portfolio demonstration purposes. It is not intended to provide medical diagnosis, treatment recommendations, or professional medical advice.

---

## Overview

The Medical Appointment System was developed to explore the design of a full-stack application that integrates RESTful APIs, database persistence, authentication, containerization, and AI-assisted information retrieval.

The application separates the frontend and backend into independent services. The FastAPI backend manages application logic and API endpoints, while the Streamlit frontend provides the user interface. PostgreSQL is used for persistent application data, and ChromaDB supports the AI assistant's retrieval and caching workflow.

The project demonstrates how traditional software engineering components can be combined with modern AI technologies to build an integrated application.

---

## Features

### Appointment Management

* Create medical appointments
* View scheduled appointments
* Store appointment information in PostgreSQL
* Manage appointment-related operations through REST APIs

### AI-Assisted Healthcare Information

* Natural-language interaction with an AI assistant
* Retrieval-Augmented Generation (RAG) workflow
* Semantic similarity search
* Vector-based information retrieval
* Response caching using ChromaDB

### Authentication

* User authentication
* Protected application functionality
* Authentication logic integrated with the FastAPI backend

### User Interface

* Interactive Streamlit web application
* Appointment management interface
* AI assistant interface
* Integration with backend REST APIs

### Containerization

* Dockerized backend
* Dockerized frontend
* Docker Compose configuration
* Consistent local development environment

---

## System Architecture

```text
                         User
                           |
                           v
                +---------------------+
                |   Streamlit         |
                |   Frontend          |
                +----------+----------+
                           |
                           | REST API
                           v
                +---------------------+
                |     FastAPI         |
                |      Backend        |
                +----------+----------+
                           |
              +------------+------------+
              |                         |
              v                         v
     +----------------+        +----------------+
     |   PostgreSQL   |        |  AI Services   |
     |    Database    |        |                |
     +----------------+        +-------+--------+
                                       |
                                       v
                                +--------------+
                                |   ChromaDB   |
                                | Vector Search|
                                | & Caching    |
                                +--------------+
```

---

## AI Workflow

The AI assistant uses a retrieval and response-caching workflow.

```text
User Question
      |
      v
Check ChromaDB Cache
      |
      +-------------------------+
      |                         |
      v                         v
Cached Response             No Cache
      |                         |
      v                         v
Return Response          Generate AI Response
                                |
                                v
                         Store Response
                           in ChromaDB
                                |
                                v
                         Return Response
```

This workflow allows previously processed queries to be retrieved from the vector store rather than repeatedly generating the same response.

---

## Technology Stack

| Category             | Technologies                            |
| -------------------- | --------------------------------------- |
| Programming Language | Python                                  |
| Backend              | FastAPI, Uvicorn                        |
| Frontend             | Streamlit                               |
| Database             | PostgreSQL                              |
| Database Platform    | Supabase                                |
| ORM                  | SQLAlchemy                              |
| AI / RAG             | Mistral, Retrieval-Augmented Generation |
| Vector Storage       | ChromaDB                                |
| API Architecture     | REST                                    |
| Containerization     | Docker, Docker Compose                  |
| Version Control      | Git, GitHub                             |

---

## Project Structure

```text
medical-appointment-system/
|
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
|
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
|
├── .gitignore
├── docker-compose.yml
└── README.md
```

### Backend Components

| File                 | Purpose                                   |
| -------------------- | ----------------------------------------- |
| `main.py`            | FastAPI application and API routes        |
| `auth.py`            | Authentication functionality              |
| `database.py`        | Database connection and configuration     |
| `models.py`          | Database models                           |
| `schemas.py`         | API request and response schemas          |
| `ai_service.py`      | AI-related application logic              |
| `agent_service.py`   | AI agent and workflow functionality       |
| `chroma_cache.py`    | ChromaDB integration and response caching |
| `assistant_tools.py` | Tools used by the AI assistant            |

---

## API

The application exposes RESTful endpoints for core application functionality.

Examples include:

```text
POST /appointments
GET  /appointments
POST /login
POST /chat
```

FastAPI provides interactive API documentation through Swagger UI.

When running locally:

```text
http://localhost:8000/docs
```

---

## Getting Started

### Prerequisites

Install the following before running the application:

* Python 3.10 or later
* PostgreSQL
* Docker Desktop
* Git

---

### Clone the Repository

```bash
git clone https://github.com/juliagrace07/medical-appointment-system.git
cd medical-appointment-system
```

---

## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
pip install -r requirements.txt
```

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will provide the local URL for accessing the application.

---

## Docker

The application includes Docker configuration for the frontend and backend services.

From the project root:

```bash
docker compose up --build
```

To stop the application:

```bash
docker compose down
```

---

## Environment Variables

The application uses environment variables for configuration and credentials.

Create a local `.env` file based on the required configuration.

Example:

```text
DATABASE_URL=
SUPABASE_URL=
SUPABASE_KEY=
MODEL_API_KEY=
```

Do not commit `.env` files, API keys, passwords, database credentials, or other sensitive information to the repository.

A `.env.example` file can be used to document required environment variables without exposing credentials.

---

## Screenshots

Screenshots demonstrating the application interface and API documentation will be added here.

### Application Dashboard

![Application Dashboard](docs/images/dashboard.png)

### Appointment Management

![Appointment Management](docs/images/appointments.png)

### AI Assistant

![AI Assistant](docs/images/ai-assistant.png)

### API Documentation

![API Documentation](docs/images/api-docs.png)

---

## Testing

Automated testing is being added to validate core application functionality, API behavior, and appointment-management workflows.

The planned test suite will use `pytest`.

```bash
pytest
```

---

## Future Improvements

* Doctor availability management
* Expanded role-based access control
* Appointment reminders
* Calendar integration
* Analytics dashboard
* Cloud deployment
* Expanded automated test coverage
* AI retrieval evaluation
* Application monitoring
* Improved production deployment configuration

---

## Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* REST API development
* FastAPI application architecture
* Database modeling
* PostgreSQL integration
* Authentication
* Full-stack application development
* Frontend/backend separation
* Docker containerization
* RESTful API design
* Vector search
* Retrieval-Augmented Generation
* AI response caching
* API documentation
* Software architecture

---

## Author

**Julia Grace Muddada**

M.S. Computer Science | Wright State University

* GitHub: [juliagrace07](https://github.com/juliagrace07)
* LinkedIn: [Julia Grace Muddada](https://www.linkedin.com/in/julia-grace-muddada-6708271b3/)

---

## Project Status

**Active portfolio project**

The application is being continuously improved with additional testing, documentation, deployment, and software engineering practices.
