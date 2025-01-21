import sys
import os
# Proje kök dizinini Python path'e ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
import aiosqlite
from passlib.hash import bcrypt
from sanic import Sanic, response
from sanic.response import json, html, redirect, file
from sanic_ext import Extend
from jinja2 import Environment, FileSystemLoader
from app.database import init_db
from app.routes.auth import auth_bp
from app.routes.customer import customer_bp
from app.routes.barber import barber_bp

app = Sanic("BarberReservation")

# Database bağlantısı
@app.listener("before_server_start")
async def setup_db(app, loop):
    app.ctx.db = await aiosqlite.connect("barber.db")
    print("Veritabanı bağlantısı kuruldu.")

@app.listener("after_server_stop")
async def close_db(app, loop):
    await app.ctx.db.close()
    print("Veritabanı bağlantısı kapatıldı.")

@app.route("/")
async def index(request):
    return await file("index.html")

# Kullanıcı Girişi
@app.route("/login", methods=["POST"])
async def login(request):
    data = request.json
    email = data.get("email")
    password = data.get("password")

    async with app.ctx.db.execute("SELECT id, password FROM users WHERE email = ?", (email,)) as cursor:
        user = await cursor.fetchone()
        if user and bcrypt.verify(password, user[1]):
            return response.json({"message": "Giriş başarılı", "user_id": user[0]}, status=200)
    return response.json({"message": "E-posta veya şifre yanlış"}, status=401)

# Kullanıcı Kaydı
@app.route("/register", methods=["POST"])
async def register(request):
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone = data.get("phone")
    email = data.get("email")
    password = bcrypt.hash(data.get("password"))

    try:
        await app.ctx.db.execute(
            "INSERT INTO users (first_name, last_name, phone, email, password) VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, phone, email, password)
        )
        await app.ctx.db.commit()
        return response.json({"message": "Kayıt başarılı"}, status=201)
    except Exception as e:
        return response.json({"message": "Kayıt sırasında bir hata oluştu", "error": str(e)}, status=400)

# Randevu Oluşturma
@app.route("/create-reservation", methods=["POST"])
async def create_reservation(request):
    data = request.json
    user_id = data.get("user_id")
    date = data.get("date")
    time = data.get("time")
    service = data.get("service")

    try:
        await app.ctx.db.execute(
            "INSERT INTO barber_schedule (user_id, date, time, service) VALUES (?, ?, ?, ?)",
            (user_id, date, time, service)
        )
        await app.ctx.db.commit()
        return response.json({"message": "Randevu oluşturuldu"}, status=201)
    except Exception as e:
        return response.json({"message": "Randevu oluşturulurken bir hata oluştu", "error": str(e)}, status=400)

# Berber Takvimi
@app.route("/barber-schedule", methods=["GET"])
async def barber_schedule(request):
    async with app.ctx.db.execute("SELECT date, time, service FROM barber_schedule") as cursor:
        schedule = await cursor.fetchall()
        return response.json({"schedule": [dict(date=row[0], time=row[1], service=row[2]) for row in schedule]}, status=200)

# Statik dosya servisi
@app.route("/styles.css")
async def serve_styles(request):
    return await file("styles.css")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
