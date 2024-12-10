# Base image for development
FROM python:3.12-slim AS base

ENV DJANGO_SETTINGS_MODULE=bab.settings

# Creates application directory
WORKDIR /app

# Creates an appuser and change the ownership of the application's folder
RUN useradd appuser && chown appuser ./ && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

# Copy dependency definition to cache
COPY --chown=appuser poetry.lock pyproject.toml ./

# Copies and chowns for the userapp on a single layer
COPY --chown=appuser . ./

# Development stage
FROM base AS development

# Install development dependencies
RUN poetry install --no-root

# Command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

# Testing stage
FROM base AS testing

# Install testing dependencies
RUN poetry install --no-root

# Command to run tests
CMD ["pytest"]

# Production stage
FROM base AS production

# Install production dependencies
RUN poetry install --no-root --without dev

EXPOSE 8080

# Command to run the production server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]