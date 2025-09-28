FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p static/uploads

# Expose port
EXPOSE 8000

# Command to run the application
CMD bash -c "echo \"Waiting for MySQL...\"; \
    while ! mysqladmin ping -h\"mysql\" --silent; do \
        sleep 1; \
    done; \
    echo \"MySQL is up!\"; \
    echo \"Applying database migrations...\"; \
    alembic upgrade head; \
    echo \"Seeding dummy data...\"; \
    mysql -u root -p\"$MYSQL_ROOT_PASSWORD\" social_scheduler < scripts/dummy_seed.sql; \
    echo \"Starting backend application...\"; \
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"