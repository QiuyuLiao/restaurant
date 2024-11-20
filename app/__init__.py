from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Configure SQLite database path (if needed)
    database_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'restaurant.db')

    # Add a secret key for sessions
    app.secret_key = "my_super_secret_key_12345"  # Replace this with a random secure key for local use

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
