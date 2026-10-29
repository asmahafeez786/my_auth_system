from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from models import db, bcrypt

from routes import register_routes


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)


jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    print("DATABASE LOCATION:", db.engine.url.database)

register_routes(app)


if __name__ == "__main__":
    app.run(debug=True)