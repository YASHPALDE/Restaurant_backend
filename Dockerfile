# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create media directory
RUN mkdir -p /app/media

# Run migrations and collect static files (Note: migrations on sqlite in docker might lose data if not using volumes)
# For Render, you might want to run these as part of the release command or startup
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# Expose port (Render will override this with $PORT)
EXPOSE 8000

# Start migrations and then gunicorn
CMD python manage.py migrate && gunicorn --bind 0.0.0.0:8000 config.wsgi:application
