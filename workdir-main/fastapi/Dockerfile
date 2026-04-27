FROM python:3.11-slim
WORKDIR /app
COPY fastapi/requirements.txt .
RUN pip install -r requirements.txt
COPY fastapi/ .
COPY data/ ./data/
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
