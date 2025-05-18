from flask import Flask
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from flask_restx import Api
from resources.auth import api as auth_ns
from resources.wallet import api as wallet_ns
from resources.admin import api as admin_ns

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

api = Api(app, title="Digital Wallet System", doc="/docs")
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(wallet_ns, path="/wallet")
api.add_namespace(admin_ns, path="/admin")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
