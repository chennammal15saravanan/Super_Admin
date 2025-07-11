from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

app = Flask(__name__, template_folder="templates")
CORS(app)
# ✅ Supabase Configuration
SUPABASE_URL = "https://fpzjwfrdqmwvpieysvbo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwemp3ZnJkcW13dnBpZXlzdmJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2MjAzMTgsImV4cCI6MjA2NTE5NjMxOH0.oz3mhk_PAWuodODGIHFUEv93quWQRhMwe6agBmDD2vU"  # NOT the anon key
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



# ✅ Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password_input = data['password']

    try:
        response = supabase.table("admins").select("*").eq("email", email).execute()
        if response.data:
            user = response.data[0]
            if check_password_hash(user['password'], password_input):
                return jsonify({'status': 'success', 'message': f"Welcome back, {user['username']}!"})
            else:
                return jsonify({'status': 'error', 'message': 'Incorrect password'})
        else:
            return jsonify({'status': 'error', 'message': 'Email not found'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# ✅ Run the server
if __name__ == "__main__":
    app.run(debug=True)
