FROM python:3.9.10-slim as builder

WORKDIR /app
ENV STAGE=${STAGE} \
  POETRY_VERSION=1.0.0

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY ./poetry.lock ./pyproject.toml ./

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$STAGE" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . .

# copy entrypoint.sh
COPY ./entrypoint.sh /app/entrypoint.sh

# copy project
COPY . /app

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:7000" ]
