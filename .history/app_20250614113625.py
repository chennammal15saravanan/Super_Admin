from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

app = Flask(__name__, template_folder="templates")
CORS(app)

# ✅ Serve frontend HTML at root
@app.route("/")
def home():
    return render_template("loginsignup.html")  # Your login/signup page

# ✅ Dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")  # Page after successful login

# ✅ Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password TEXT
    )''')
    conn.commit()
    conn.close()

# ✅ Password hashing (SHA256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Signup endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    email = data['email']
    password = hash_password(data['password'])

    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (username, email, password))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'User registered successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Email already exists'})
    finally:
        conn.close()

# ✅ Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = hash_password(data['password'])

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({'status': 'success', 'message': f'Welcome back, {user[1]}!'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid email or password'})

# ✅ Start server
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
