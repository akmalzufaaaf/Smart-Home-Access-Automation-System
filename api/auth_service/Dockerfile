# Gunakan image dasar Python
FROM python:3.13-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin semua file project ke dalam container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Buka port aplikasi
EXPOSE 5000

# Jalankan service
CMD ["python", "app.py"]
