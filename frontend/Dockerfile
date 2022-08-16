FROM python:3.10

WORKDIR /app

ENV STAGE=${STAGE} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY app/poetry.lock app/pyproject.toml ./

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$STAGE" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY app/ .