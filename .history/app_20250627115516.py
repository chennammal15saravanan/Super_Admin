from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

app = Flask(__name__, template_folder="templates")
CORS(app)

# ✅ Supabase Configuration
SUPABASE_URL = "https://fpzjwfrdqmwvpieysvbo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwemp3ZnJkcW13dnBpZXlzdmJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2MjAzMTgsImV4cCI6MjA2NTE5NjMxOH0.oz3mhk_PAWuodODGIHFUEv93quWQRhMwe6agBmDD2vU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Serve frontend HTML at root
@app.route("/")
def home():
    return render_template("loginsignup.html")

# ✅ Dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Users list view
@app.route('/users')
def users():
    resp = supabase.table("users").select("username, email").execute()
    users = resp.data or []
    return render_template("users.html", users=users)

# User datasets view
@app.route('/users/<user_id>/queries')
def user_datasets(user_id):
    resp = supabase.table("datasets").select("dataset_id, dataset_name, created_at").eq("user_id", user_id).execute()
    return render_template("user_datasets.html", datasets=resp.data or [], user_id=user_id)

# User uploads view
@app.route('/users/<user_id>/uploads')
def user_uploads(user_id):
    resp = supabase.table("file_uploads").select("file_id, file_name, upload_time").eq("user_id", user_id).execute()
    return render_template("user_uploads.html", uploads=resp.data or [], user_id=user_id)




# ✅ Sign-Up Endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    # Check for existing email
    try:
        check_user = supabase.table("admins").select("*").eq("email", email).execute()
        if check_user.data:
            return jsonify({'status': 'error', 'message': 'Email already exists'})
        
    
        # Insert new user
        response = supabase.table("admins").insert({
            "id": user_id,
            "username": username,
            "email": email,
            "password": password,
            "created_at": created_at
        }).execute()

        if response.data:
            return jsonify({'status': 'success', 'message': 'User registered successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Registration failed'}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ✅ Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password_input = data.get('password')

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

# ✅ Run server
if __name__ == "__main__":
    app.run(debug=True)
