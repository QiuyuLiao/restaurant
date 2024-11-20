from flask import Blueprint, request, jsonify, render_template
from .db_utils import add_user, get_all_users, get_user_by_email, update_user, delete_user

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

# Route to update a user
@main.route('/update_user/<int:userid>', methods=['PUT'])
def update_user_route(userid):
    data = request.get_json()

    # Extract user data from the request
    username = data.get('username')
    phone_number = data.get('phone_number')
    is_admin = data.get('isAdmin', False)

    if not username or not phone_number:
        return jsonify({"error": "All fields (username, phone_number) are required"}), 400

    # Update the user in the database
    update_user(userid, username, phone_number, is_admin)
    return jsonify({"message": f"User {userid} updated successfully!"})

# Route to delete a user
@main.route('/delete_user/<int:userid>', methods=['DELETE'])
def delete_user_route(userid):
    delete_user(userid)
    return jsonify({"message": f"User {userid} deleted successfully!"})
