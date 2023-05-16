from app import create_app
from app import db

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    # Create the database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run()   