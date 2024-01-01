# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.1
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install application dependencies with pip
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Ensure gunicorn is installed in the base image
RUN pip install gunicorn

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the source code into the container.
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Ensure the user has permission to write to the application directory
RUN chown -R appuser:appuser /app

# Use non-root user to run the application
USER appuser

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
