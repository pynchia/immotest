
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 as base
ENV PORT="8080"
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM base as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . /app
RUN poetry install --no-interaction --no-ansi -vvv --without dev

# FROM base as runtime
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
EXPOSE 8080
