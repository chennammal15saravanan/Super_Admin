from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

app = Flask(__name__, template_folder="templates")
app.secret_key = 'your-secret-key'  # Required for session management
CORS(app)

# ✅ Supabase Configuration
SUPABASE_URL = "https://swrhcsfuorjqszqoohfb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN3cmhjc2Z1b3JqcXN6cW9vaGZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5MTgwNzAsImV4cCI6MjA2NjQ5NDA3MH0.Th0bFIOF5Xrrk6oSQKeRGxDwYSJxkcJvksxQla4vIZM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Serve frontend HTML at root
@app.route("/")
def home():
    return render_template("loginsignup.html")

# ✅ Dashboard route (requires admin login)
@app.route("/dashboard")
def dashboard():
    if 'admin_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in as admin'}), 401
    resp = supabase.table("users").select("user_id, username, email").execute()
    users = resp.data or []
    return render_template("dashboard.html", users=users)

# Users list view (admin only)
@app.route('/users')
def users():
    if 'admin_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in as admin'}), 401
    resp = supabase.table("users").select("user_id, username, email").execute()
    users = resp.data or []
    return render_template("users.html", users=users)

#  Queries endpoint using user_id from users table
@app.route("/api/users/<user_id>/queries")
def get_user_queries(user_id):
    query_resp = supabase.table("queries").select("*").eq("user_id", user_id).execute()
    queries = query_resp.data

    if not queries:
        user_resp = supabase.table("users").select("").eq("user_id", user_id).single().execute()
        user = user_resp.data
        username = user.get("username", "User")
        email = user.get("email", "")
        return f"<p>No queries found for {username} ({email}).</p>"

    html = "<ul>"
    for q in queries:
        html += f"<li>{q['query_text']}</li>"
    html += "</ul>"
    return html


# ✅ Responses endpoint using user_id from users table
@app.route('/api/users/<user_id>/responses')
def get_user_responses(user_id):
    user_resp = supabase.table("users").select("*").eq("user_id", user_id).execute()
    if not user_resp.data:
        return "<p>User not found.</p>"

    user = user_resp.data[0]
    responses_resp = supabase.table("responses").select("*").eq("user_id", user_id).execute()
    responses = responses_resp.data or []

    if not responses:
        return f"<p>No responses found for {user['username']} ({user['email']}).</p>"

    html = f"<h3>Responses for {user['username']} ({user['email']})</h3><ul>"
    for r in responses:
        html += f"<li>{r['response_text']} (at {r['timestamp']})</li>"
    html += "</ul>"

    return html

# ✅ Sign-Up Endpoint for admins
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    # Check for existing email in admins table
    try:
        check_user = supabase.table("admins").select("*").eq("email", email).execute()
        if check_user.data:
            return jsonify({'status': 'error', 'message': 'Email already exists'})
        
        # Insert new admin
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

# ✅ Login Endpoint for admins
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
                session['admin_id'] = user['id']  # Store admin session
                return jsonify({'status': 'success', 'message': f"Welcome back, {user['username']}!"})
            else:
                return jsonify({'status': 'error', 'message': 'Incorrect password'})
        else:
            return jsonify({'status': 'error', 'message': 'Email not found'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# ✅ Logout Endpoint
@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})

# ✅ Run server
if __name__ == "__main__":
    app.run(debug=True)