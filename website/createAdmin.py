from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create new admin user
    new_admin = User(
        email='admin@kkumail.com',
        userName='Admin',
        password=generate_password_hash('Admin', method='pbkdf2:sha256'),
        is_admin=True
    )
    
    db.session.add(new_admin)
    db.session.commit()
    print("New admin user created successfully!")