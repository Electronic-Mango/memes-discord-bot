# Dockerfile which can be used for deploying the bot as a Docker container.

FROM python:3.10-alpine

RUN apk add gcc g++ musl-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY *.yml .

CMD ["python", "src/main.py"]
