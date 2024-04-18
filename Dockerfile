FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY src/ src/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python3", "src/app.py"]

