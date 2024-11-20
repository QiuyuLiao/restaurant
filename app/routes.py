from flask import Blueprint, request, jsonify, render_template, redirect, session
from .db_utils import (
    add_user, get_all_users, get_user_by_email, update_user, delete_user,
    add_table, get_all_tables, update_table, delete_table, authenticate_user,
    reserve_table, cancel_reservation, get_user_order_history, add_review, get_reviews_by_table
)

main = Blueprint('main', __name__)

# Secure sessions
@main.before_request
def secure_session():
    session.permanent = True

# Route for the login/register page (New Home Page)
@main.route('/')
def home():
    return render_template('login.html')  # Login and Registration form

# Login route
@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Authenticate user
    user = authenticate_user(email, password)
    if user:
        session['user_id'] = user['userid']
        session['is_admin'] = user['isAdmin']

        # Redirect based on user role
        if user['isAdmin']:
            return redirect('/admin')  # Redirect to admin dashboard
        else:
            return redirect('/booking')  # Redirect to booking page
    return jsonify({"error": "Invalid email or password"}), 401

# Logout route
@main.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to the homepage (login page)
    return redirect('/')

# Registration route
@main.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    phone_number = request.form.get('phone_number')

    if not email or not username or not password or not phone_number:
        return jsonify({"error": "All fields are required"}), 400

    add_user(email, username, password, phone_number)
    return redirect('/')  # Redirect to login page after registration

# Admin Dashboard
@main.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect('/')  # Redirect to login if not admin
    users = get_all_users()
    tables = get_all_tables()
    return render_template('index.html', users=users, tables=tables)

# Booking Page
@main.route('/booking')
def booking():
    if not session.get('user_id'):
        return redirect('/')  # Redirect to login if not logged in
    tables = get_all_tables()
    return render_template('booking.html', tables=tables)

# Order History Page
@main.route('/order_history')
def order_history():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')  # Redirect to login if not logged in

    # Fetch the user's order history
    history = get_user_order_history(user_id)
    return render_template('order_history.html', history=history)

# Route to reserve a table
@main.route('/reserve_table/<int:table_id>', methods=['POST'])
def reserve_table_route(table_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 403

    reserve_table(user_id, table_id)
    return redirect('/booking')

# Route to cancel a reservation
@main.route('/cancel_reservation/<int:table_id>', methods=['POST'])
def cancel_reservation_route(table_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 403

    cancel_reservation(user_id, table_id)
    return redirect('/booking')

# Route to add a review
@main.route('/add_review/<int:table_id>', methods=['POST'])
def add_review_route(table_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 403

    review_text = request.form.get('review_text')
    if not review_text:
        return jsonify({"error": "Review text is required"}), 400

    add_review(user_id, table_id, review_text)
    return redirect('/order_history')

# Route to view reviews for a table
@main.route('/view_reviews/<int:table_id>')
def view_reviews_route(table_id):
    reviews = get_reviews_by_table(table_id)
    if not reviews:
        return render_template('reviews.html', message="No reviews available for this table.")
    return render_template('reviews.html', reviews=reviews)

# User-related routes
@main.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    phone_number = data.get('phone_number')
    is_admin = data.get('isAdmin', False)

    if not email or not username or not password or not phone_number:
        return jsonify({"error": "All fields (email, username, password, phone_number) are required"}), 400

    add_user(email, username, password, phone_number, is_admin)
    return jsonify({"message": f"User {username} added successfully!"})

@main.route('/update_user/<int:userid>', methods=['PUT'])
def update_user_route(userid):
    data = request.get_json()
    username = data.get('username')
    phone_number = data.get('phone_number')
    is_admin = data.get('isAdmin', False)

    if not username or not phone_number:
        return jsonify({"error": "All fields (username, phone_number) are required"}), 400

    update_user(userid, username, phone_number, is_admin)
    return jsonify({"message": f"User {userid} updated successfully!"})

@main.route('/delete_user/<int:userid>', methods=['DELETE'])
def delete_user_route(userid):
    delete_user(userid)
    return jsonify({"message": f"User {userid} deleted successfully!"})

# Table-related routes
@main.route('/add_table', methods=['POST'])
def add_table_route():
    data = request.get_json()
    isAvailable = data.get('isAvailable', True)
    capacity = data.get('capacity')

    if capacity is None:
        return jsonify({"error": "Capacity is required"}), 400

    add_table(isAvailable, capacity)
    return jsonify({"message": "Table added successfully!"})

@main.route('/update_table/<int:table_id>', methods=['PUT'])
def update_table_route(table_id):
    data = request.get_json()
    isAvailable = data.get('isAvailable')
    capacity = data.get('capacity')

    if capacity is None or isAvailable is None:
        return jsonify({"error": "Both isAvailable and capacity are required"}), 400

    update_table(table_id, isAvailable, capacity)
    return jsonify({"message": f"Table {table_id} updated successfully!"})

@main.route('/delete_table/<int:table_id>', methods=['DELETE'])
def delete_table_route(table_id):
    delete_table(table_id)
    return jsonify({"message": f"Table {table_id} deleted successfully!"})
