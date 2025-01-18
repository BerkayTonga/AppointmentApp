# Dockerfile

# Python 3.9 slim tabanlı bir Docker imajı kullanılıyor
FROM python:3.9-slim

# Çalışma dizinini belirtiyoruz
WORKDIR /app

# Gereksinim dosyasını kopyalıyoruz
COPY requirements.txt requirements.txt
# Gerekli Python kütüphanelerini yüklüyoruz
RUN pip install -r requirements.txt

# Uygulama dosyalarını kopyalıyoruz
COPY . .

# Uygulama başlatma komutunu belirtiyoruz
CMD ["python", "app.py"]