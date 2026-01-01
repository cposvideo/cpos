FROM python:3.11-slim
WORKDIR /app
COPY src ./src
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python","-m","uvicorn","src.api.main:app","--host","0.0.0.0","--port","8000"]
