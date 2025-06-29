FROM python:3.11-slim

# Install libGL dan dependensi multimedia
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set direktori kerja
WORKDIR /app

# Copy semua file
COPY . .

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Jalankan aplikasi Flask pakai gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
