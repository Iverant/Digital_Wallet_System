from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Transaction
from utils.fraud import check_fraud

api = Namespace("wallet", description="Wallet operations")

txn_model = api.model("Transaction", {
    "amount": fields.Float(required=True)
})

transfer_model = api.model("Transfer", {
    "to_username": fields.String(required=True),
    "amount": fields.Float(required=True)
})

@api.route("/deposit")
class Deposit(Resource):
    @api.expect(txn_model)
    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        amount = request.json.get("amount")
        if amount <= 0:
            return {"msg": "Amount must be positive"}, 400
        user.balance += amount
        txn = Transaction(type="deposit", amount=amount, receiver_id=user.id)
        db.session.add(txn)
        db.session.commit()
        return {"msg": "Deposited", "balance": user.balance}, 200

@api.route("/withdraw")
class Withdraw(Resource):
    @api.expect(txn_model)
    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        amount = request.json.get("amount")
        if amount <= 0 or amount > user.balance:
            return {"msg": "Invalid withdrawal amount"}, 400
        user.balance -= amount
        txn = Transaction(type="withdraw", amount=amount, sender_id=user.id)
        db.session.add(txn)
        db.session.commit()
        return {"msg": "Withdrawn", "balance": user.balance}, 200

@api.route("/transfer")
class Transfer(Resource):
    @api.expect(transfer_model)
    @jwt_required()
    def post(self):
        sender = User.query.get(get_jwt_identity())
        data = request.json
        amount = data["amount"]
        receiver = User.query.filter_by(username=data["to_username"]).first()

        if not receiver or amount <= 0 or amount > sender.balance:
            return {"msg": "Invalid transfer"}, 400

        sender.balance -= amount
        receiver.balance += amount

        txn = Transaction(type="transfer", amount=amount, sender_id=sender.id, receiver_id=receiver.id)
        db.session.add(txn)
        check_fraud(sender.id, db)
        db.session.commit()

        return {"msg": "Transferred", "balance": sender.balance}, 200

@api.route("/history")
class History(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        txns = Transaction.query.filter((Transaction.sender_id == user_id) | (Transaction.receiver_id == user_id)).all()
        return [{
            "id": t.id,
            "type": t.type,
            "amount": t.amount,
            "timestamp": t.timestamp.isoformat(),
            "flagged": t.flagged
        } for t in txns], 200
