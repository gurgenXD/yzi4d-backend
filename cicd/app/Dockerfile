FROM python:3.11-bullseye

ARG WORK_DIR=/opt/mnt

ENV PYTHONUNBUFFERED=on
ENV PYTHONPATH=${WORK_DIR}
ENV POETRY_VERSION=1.3.2

RUN pip install --upgrade pip && pip install "poetry==$POETRY_VERSION"

WORKDIR ${WORK_DIR}

COPY pyproject.toml poetry.lock ${WORK_DIR}

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY . ${WORK_DIR}
