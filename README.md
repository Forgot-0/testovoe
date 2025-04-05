# Testovoe

## Features

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
- **Alembic**: Database migrations for SQLAlchemy.
- **Redis**: Used for caching and task queues.
- **TaskIQ**: Task queue and scheduler integration.
- **Loguru**: Advanced logging setup.
- **PostgreSQL**: Database backend.
- **Docker**: Containerized development and deployment.
- **Pydantic**: Data validation and settings management.

## Project Structure

```plaintext
.
├── app/
│   ├── core/               # Core utilities and services
│   ├── secret/             # Secret management module
│   ├── main.py             # Application entry point
├── migrations/             # Alembic migrations
├── .env                    # Environment variables
├── docker-compose.yaml     # Docker Compose configuration
├── Dockerfile              # Dockerfile for the application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.12
- Docker and Docker Compose

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd testovoe
    ```

2. Create a `.env` file based on `.env.example`:
    ```bash
    cp .env.example .env
    ```

3. Build and start the services using Docker Compose:
    ```bash
    docker-compose up --build
    ```

4. Access the application at `http://localhost:8000`.


### API Documentation

The API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`

