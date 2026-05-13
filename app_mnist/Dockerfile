FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libgl1

COPY . .

CMD ["python", "asgi.py"]