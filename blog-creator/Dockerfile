FROM python:3.9-slim

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . .

ENV PYTHONPATH=/app

# COPY --chown=user app/files/.env .env
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]