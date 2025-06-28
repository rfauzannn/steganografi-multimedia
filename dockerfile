FROM python:3.11-slim

# Install libGL dan dependensi
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Copy project
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Jalankan app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
