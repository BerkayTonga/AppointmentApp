from sanic import Sanic, response
from sanic_ext import Extend
import pyodbc

app = Sanic("BerberApp")
Extend(app)

# SQL Server bağlantı ayarları
SQL_SERVER_CONNECTION = (
    "DRIVER = {ODBC Driver 17 for SQL Server};"
    "SERVER = localhost;"  # SQL Server'ın çalıştığı sunucu (örneğin: localhost veya IP adresi)
    "DATABASE = BerberAppDB;"  # Veritabanı adı
    "UID = sa;"  # SQL Server kullanıcı adı (varsayılan: 'sa' olabilir)
    "PWD = your_password;"  # SQL Server şifresi
)

def get_db_connection():
    return pyodbc.connect(SQL_SERVER_CONNECTION)

@app.post("/api/login")
async def login(request):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE username=? AND password=?", (data['username'], data['password']))
    user = cursor.fetchone()
    conn.close()
    if user:
        user_data = {"id": user[0], "username": user[1], "email": user[2]}
        return response.json({"success": True, "user": user_data})
    return response.json({"success": False})

@app.post("/api/register")
async def register(request):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (data['username'], data['password'], data['email']))
        conn.commit()
        conn.close()
        return response.json({"success": True})
    except Exception as e:
        conn.close()
        return response.json({"success": False, "error": str(e)})

@app.get("/api/appointments")
async def get_appointments(request):
    date = request.args.get('date')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, time FROM appointments WHERE date=?", (date,))
    appointments = cursor.fetchall()
    conn.close()
    return response.json([{"id": row[0], "date": row[1], "time": row[2]} for row in appointments])

@app.post("/api/appointments")
async def create_appointment(request):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO appointments (date, time) VALUES (?, ?)", (data['date'], data['time']))
        conn.commit()
        conn.close()
        return response.json({"success": True})
    except Exception as e:
        conn.close()
        return response.json({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
