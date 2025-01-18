from sanic import Sanic
from sanic.response import json, html, redirect
from app.database import init_db
from routes.auth import auth_bp
from routes.customer import customer_bp
from routes.barber import barber_bp

# Sanic uygulamasını oluşturuyoruz
app = Sanic("BarberAppointment")

# Blueprint'leri (alt rota gruplarını) kaydediyoruz
app.blueprint(auth_bp)
app.blueprint(customer_bp)
app.blueprint(barber_bp)

# Sunucu başlamadan önce veritabanını başlatma işlemi
@app.listener('before_server_start')
async def setup_db(app, loop):
    await init_db()

# Ana uygulamayı çalıştırıyoruz
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)