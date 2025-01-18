import aiomysql

# Veritabanını başlatmak için kullanılan fonksiyon
async def init_db():
    global pool
    pool = await aiomysql.create_pool(
        host="localhost",  # Veritabanı sunucu adresi
        port=3306,  # MySQL varsayılan portu
        user="root",  # Veritabanı kullanıcı adı
        password="password",  # Veritabanı şifresi
        db="barber_appointment",  # Kullanılacak veritabanı
        autocommit=True  # Otomatik olarak işlemleri kaydet
    )

# Veritabanı bağlantısını almak için kullanılan generator fonksiyonu
async def get_db():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            yield cur