FROM tiangolo/uvicorn-gunicorn-starlette:python3.8-alpine3.10

COPY . /app

RUN pip install -r /app/requirements-prod.txt
