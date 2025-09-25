# Backend

FastAPI, Celery, and PostgreSQL backend.

Run those commands to run the backend

## Local Development (Linux/macOS)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
celery -A app.tasks.celery worker --loglevel=info &
celery -A app.tasks.celery beat --loglevel=info
```

## Local Development (Windows)

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
start "API" cmd /c "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
start "Celery Worker" cmd /c "celery -A app.tasks.celery worker --loglevel=info"
start "Celery Beat" cmd /c "celery -A app.tasks.celery beat --loglevel=info"
```