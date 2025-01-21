import sqlite3

def create_database():
    # Veritabanını oluştur veya bağlan
    conn = sqlite3.connect('barber.db')
    cursor = conn.cursor()

    # Kullanıcı tablosunu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Randevu tablosunu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS barber_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            service TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    print("Veritabanı ve tablolar başarıyla oluşturuldu!")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
