FROM python:3.10-slim as bulider

COPY Pipfile* ./

RUN pip3 install pipenv && \
    pipenv lock --requirements > requirements.txt && \
    python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --requirement requirements.txt

FROM python:3.10-alpine

COPY --from=bulider /venv /venv

WORKDIR /app
COPY src/ycc.py .

VOLUME [ "/data", "/output" ]

ENTRYPOINT [ "/venv/bin/python3", "ycc.py" ]
