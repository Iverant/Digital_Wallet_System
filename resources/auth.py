from flask import request
from flask_restx import Resource, Namespace, fields
from models import db, User
import bcrypt
from flask_jwt_extended import create_access_token

api = Namespace("auth", description="Authentication")

auth_model = api.model("Auth", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})

@api.route("/register")
class Register(Resource):
    @api.expect(auth_model)
    def post(self):
        data = request.json
        if User.query.filter_by(username=data['username']).first():
            return {"msg": "Username already exists"}, 400
        hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        user = User(username=data['username'], password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return {"msg": "Registered successfully"}, 201

@api.route("/login")
class Login(Resource):
    @api.expect(auth_model)
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if not user or not bcrypt.checkpw(data['password'].encode(), user.password_hash):
            return {"msg": "Invalid credentials"}, 401
        token = create_access_token(identity=user.id)
        return {"access_token": token}, 200
