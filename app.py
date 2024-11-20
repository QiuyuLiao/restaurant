from app import create_app

app = create_app()
app.secret_key = "my_super_secret_key_12345"  # Just make something up

if __name__ == "__main__":
    app.run(debug=True)
