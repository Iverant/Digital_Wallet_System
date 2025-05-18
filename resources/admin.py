from flask_restx import Resource, Namespace
from models import db, Transaction, User

api = Namespace("admin", description="Admin Reporting")

@api.route("/flagged")
class FlaggedTxns(Resource):
    def get(self):
        flagged = Transaction.query.filter_by(flagged=True).all()
        return [{"id": t.id, "type": t.type, "amount": t.amount} for t in flagged], 200

@api.route("/balances")
class TotalBalance(Resource):
    def get(self):
        total = db.session.query(db.func.sum(User.balance)).scalar() or 0.0
        return {"total_balance": total}, 200

@api.route("/top-users")
class TopUsers(Resource):
    def get(self):
        users = User.query.order_by(User.balance.desc()).limit(5).all()
        return [{"username": u.username, "balance": u.balance} for u in users], 200
