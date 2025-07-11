from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

app = Flask(__name__, template_folder="templates")
CORS(app)
# ✅ Supabase Configuration
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_SERVICE_ROLE_KEY"  # NOT the anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ✅ Serve frontend HTML at root
@app.route("/")
def home():
    return render_template("loginsignup.html")  # Your login/signup page

# ✅ Dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")  # Page after successful login

# ✅ Sign-Up Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])
    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    try:
        response = supabase.table("admins").insert({
            "id": user_id,
            "username": username,
            "email": email,
            "password": password,
            "created_at": created_at
        }).execute()

        if response.status_code in [200, 201]:
            return jsonify({'status': 'success', 'message': 'User registered successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Registration failed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# ✅ Password hashing (SHA256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



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
