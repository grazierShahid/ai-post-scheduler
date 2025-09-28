# Social Post Scheduler

This is a platform to schedule social media posts with AI-suggested content.

## Prerequisites

- Docker & Docker Compose
- Node.js (for local frontend development)
- Python (for local backend development)

## Run with Docker (Recommended)

This is the easiest way to run the application on any OS.

1.  **Build and run the services:**

    ```bash
    docker compose up --build -d
    ```

2.  **Apply database migrations:**

    Open a new terminal and run the following command to open a bash session in the backend container:

    ```bash
    docker compose exec backend bash
    ```

    Then, run the following command to apply the migrations:

    ```bash
    alembic revision --autogenerate -m "core db models"
    alembic upgrade head
    ```

    Exit the container session by typing `exit`.

3.  **Access the application:**

    -   Frontend: [http://localhost:3000](http://localhost:3000)
    -   Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

## Local Development

For local development, please see the README files for the `frontend` and `backend`.

-   [Backend README](./backend/README.md)
-   [Frontend README](./frontend/README.md)
