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

# ✅ Sign-Up Endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    try:
        # ✅ Supabase Auth sign-up triggers email verification
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if response.user:
            # Optionally, store extra info (like username) in your admins table
            supabase.table("admins").insert({
                "id": str(uuid.uuid4()),
                "email": email,
                "username": username,
                "created_at": datetime.utcnow().isoformat()
            }).execute()

            return jsonify({'status': 'success', 'message': 'Verification email sent. Please check your inbox.'})
        else:
            return jsonify({'status': 'error', 'message': 'Signup failed'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# ✅ Login Endpoint

# ✅ Run server
if __name__ == "__main__":
    app.run(debug=True)
