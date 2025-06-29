FROM python:3.11-slim

# Install libGL dan dep multimedia
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy semua file
COPY . .

# Upgrade pip & install python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Jalankan gunicorn (pastikan 'app.py' punya objek 'app')
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
