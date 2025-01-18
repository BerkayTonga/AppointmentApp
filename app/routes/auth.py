# routes/auth.py
from sanic import Blueprint
from sanic.response import json
import bcrypt
from database import get_db

# Kimlik doğrulama için Blueprint
auth_bp = Blueprint('auth', url_prefix='/auth')

# Kullanıcı giriş işlemi için API
@auth_bp.post('/login')
async def login(request):
    phone = request.json.get("phone")  # Kullanıcıdan gelen telefon numarası
    password = request.json.get("password")  # Kullanıcıdan gelen şifre

    query = "SELECT * FROM users WHERE phone = %s"  # Telefon numarasıyla kullanıcıyı bul
    async for cur in get_db():
        await cur.execute(query, (phone,))
        user = await cur.fetchone()

    # Şifre doğrulama ve kullanıcı giriş kontrolü
    if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
        return json({"status": "success", "message": "Login successful"})
    return json({"status": "fail", "message": "Invalid credentials"}, status=401)

# Kullanıcı kayıt işlemi için API
@auth_bp.post('/register')
async def register(request):
    name = request.json.get("name")  # Kullanıcı adı
    phone = request.json.get("phone")  # Telefon numarası
    password = bcrypt.hashpw(request.json.get("password").encode(), bcrypt.gensalt()).decode()  # Şifreyi hash'le
    role = request.json.get("role")  # Kullanıcı rolü

    query = "INSERT INTO users (name, phone, password, role) VALUES (%s, %s, %s, %s)"  # Yeni kullanıcı ekleme sorgusu

    async for cur in get_db():
        try:
            await cur.execute(query, (name, phone, password, role))  # Kullanıcıyı ekle
            return json({"status": "success", "message": "Registration successful"})
        except Exception as e:
            return json({"status": "fail", "message": str(e)}, status=400)