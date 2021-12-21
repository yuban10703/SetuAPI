FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
RUN pip install --no-cache-dir pydantic motor orjson dnspython
COPY ./app /app/app