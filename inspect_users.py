from app import app, db, User

with app.app_context():
    users = User.query.all()
    if users:
        for user in users:
            print(f"Username: {user.username} - Password Hash: {user.password}")
    else:
        print("No users found in the database.")
