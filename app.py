import sys
import os
# Proje kök dizinini Python path'e ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
from sanic import Sanic
from sanic.response import json, html, redirect
from sanic_ext import Extend
from jinja2 import Environment, FileSystemLoader
from app.database import init_db
from app.routes.auth import auth_bp
from app.routes.customer import customer_bp
from app.routes.barber import barber_bp

# Sanic uygulamasını oluşturuyoruz
app = Sanic("BarberAppointment")

# Jinja2 şablon motorunu yapılandırma
Extend(app)
app.ext.template_environment = Environment(loader=FileSystemLoader('./app/templates'))

# Blueprint'leri (alt rota gruplarını) kaydediyoruz
app.blueprint(auth_bp)
app.blueprint(customer_bp)
app.blueprint(barber_bp)

# Sunucu başlamadan önce veritabanını başlatma işlemi
@app.listener('before_server_start')
async def setup_db(app, loop):
    await init_db()

# Rota tanımlama (örnek: ana sayfa)
@app.route("/")
async def index(request):
    return html(app.ext.template("login.html"))

# Statik dosya servisini etkinleştiriyoruz
app.static('/static', './app/static')

# Ana uygulamayı çalıştırıyoruz
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
