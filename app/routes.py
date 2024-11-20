from flask import Blueprint, request, jsonify, render_template
from .db_utils import add_user, get_all_users, get_user_by_email

main = Blueprint('main', __name__)

# Route for the home page
@main.route('/')
def home():
    # Fetch all users from the database and pass to index.html
    users = get_all_users()
    return render_template('index.html', users=users)

# Route to add a new user
@main.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.get_json()

    # Extract user data from the request
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    phone_number = data.get('phone_number')
    is_admin = data.get('isAdmin', False)

    if not email or not username or not password or not phone_number:
        return jsonify({"error": "All fields (email, username, password, phone_number) are required"}), 400

    # Add the user to the database
    add_user(email, username, password, phone_number, is_admin)
    return jsonify({"message": f"User {username} added successfully!"})

# Route to get all users
@main.route('/get_users', methods=['GET'])
def get_users_route():
    users = get_all_users()
    return jsonify(users)

# Route to get a user by email
@main.route('/get_user/<email>', methods=['GET'])
def get_user_route(email):
    user = get_user_by_email(email)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404
