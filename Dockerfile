# Hafif bir Python imajı ile başlıyoruz
FROM python:3.9-slim

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Gerekli dosyaları kopyalayıp kütüphaneleri kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyalıyoruz
COPY app.py .

# Uygulamanın çalışacağı port
EXPOSE 5000

# Konteyner ayağa kalktığında çalıştırılacak komut
CMD ["python", "app.py"]