# models.py
from database import get_db

# Veritabanında tabloları oluşturmak için kullanılan fonksiyon
async def create_tables():
    query_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,  # Kullanıcı ID'si (otomatik artan)
        name VARCHAR(100) NOT NULL,  # Kullanıcı adı
        phone VARCHAR(15) UNIQUE NOT NULL,  # Telefon numarası (eşsiz)
        password VARCHAR(255) NOT NULL,  # Şifre
        role ENUM('customer', 'barber') NOT NULL  # Kullanıcı rolü (müşteri veya berber)
    )
    """
    query_appointments = """
    CREATE TABLE IF NOT EXISTS appointments (
        id INT AUTO_INCREMENT PRIMARY KEY,  # Randevu ID'si (otomatik artan)
        customer_id INT NOT NULL,  # Müşteri ID'si
        barber_id INT NOT NULL,  # Berber ID'si
        date DATE NOT NULL,  # Randevu tarihi
        time_slot TIME NOT NULL,  # Randevu saati
        services VARCHAR(255),  # Alınacak hizmetler
        notes TEXT,  # Randevu notları
        status ENUM('scheduled', 'cancelled') DEFAULT 'scheduled',  # Randevu durumu
        FOREIGN KEY (customer_id) REFERENCES users(id),  # Müşteri tablosuyla ilişki
        FOREIGN KEY (barber_id) REFERENCES users(id)  # Berber tablosuyla ilişki
    )
    """
    async for cur in get_db():
        await cur.execute(query_users)  # Kullanıcı tablosunu oluştur
        await cur.execute(query_appointments)  # Randevu tablosunu oluştur