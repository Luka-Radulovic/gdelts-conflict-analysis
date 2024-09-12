FROM python:3.12

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without dev

COPY src/gdelt_api gdelt_api
COPY alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "jitni_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
