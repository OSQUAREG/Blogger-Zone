from models import app, db
from routes import general, articles, users


# Create all DB tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True) 