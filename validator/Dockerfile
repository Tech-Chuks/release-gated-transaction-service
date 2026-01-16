FROM python:3.11-slim
WORKDIR /validator
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY validate.py checks.sql ./
CMD ["python", "validate.py"]
