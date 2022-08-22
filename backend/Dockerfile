FROM python:3.9.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# copy entrypoint.sh
COPY ./entrypoint.sh /app/entrypoint.sh

# copy project
COPY . /app

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["daphne", "backend.asgi:application", "--bind", "0:7000" ]
