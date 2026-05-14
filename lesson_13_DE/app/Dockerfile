FROM python:3.12-slim
WORKDIR /lesson_13_DE/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY utils.py .

CMD ["python", "main.py"]