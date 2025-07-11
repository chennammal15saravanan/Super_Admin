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
@app.route('/api/users/<user_id>/queries')
def get_user_queries(user_id):
    try:
        print(f"[INFO] Fetching queries for user_id: {user_id}")
        
        query_result = supabase.table("queries").select("query_text").eq("user_id", user_id).execute()
        print(f"[DEBUG] Query Result: {query_result.data}")

        if query_result.data and len(query_result.data) > 0:
            content = "<strong>Queries:</strong><ul>"
            for item in query_result.data:
                content += f"<li>{item.get('query_text', 'No text')}</li>"
            content += "</ul>"
            return content
        else:
            # Get user info for message
            user_info = supabase.table("users").select("username, email").eq("user_id", user_id).single().execute().data
            username = user_info.get("username", "Unknown User")
            email = user_info.get("email", "")
            return f"<strong>Queries</strong><br>No queries found for {username} ({email})."

    except Exception as e:
        print(f"[ERROR] Failed to fetch queries: {e}")
        return "Error loading queries: INTERNAL SERVER ERROR", 500


# Responses endpoint using user_id from users table
@app.route('/api/users/<user_id>/responses')
def get_user_responses(user_id):
    try:
        print(f"[INFO] Fetching responses for user_id: {user_id}")
        
        result = supabase.table("responses").select("*").eq("user_id", user_id).execute()
        print(f"[DEBUG] Response Query Raw Result: {result}")
        print(f"[DEBUG] Response Data: {result.data}")

        if result.data:
            content = "<strong>Responses:</strong><ul>"
            for row in result.data:
                content += f"<li>{row.get('response_text')}</li>"
            content += "</ul>"
            return content
        else:
            # Show fallback message if no responses
            user = supabase.table("users").select("username, email").eq("user_id", user_id).single().execute().data
            return f"<strong>Responses</strong><br>No responses found for {user['username']} ({user['email']})."

    except Exception as e:
        print(f"[ERROR] Failed to fetch responses: {e}")
        return "Error loading responses: INTERNAL SERVER ERROR", 500



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
       test_id = "4b15fde9-5a28-4363-80a2-92a92f20db31"
    test = supabase.table("responses").select("*").eq("user_id", test_id).execute()
    print("TEST FETCH:", test.data)
    app.run(debug=True)