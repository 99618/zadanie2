FROM python:3.12-slim AS buildpy

LABEL maintainer='Mateusz Marczak'
WORKDIR /app
COPY templates/ /app/templates/
COPY app.py requirements.txt ./

RUN pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim
LABEL maintainer='Mateusz Marczak'

WORKDIR /app
COPY --from=buildpy /install /usr/local
COPY --from=buildpy /app /app

EXPOSE 5050

HEALTHCHECK --interval=5s --timeout=1s --retries=3 CMD curl -f http://127.0.0.1:5050/ || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:5050", "app:app"]


