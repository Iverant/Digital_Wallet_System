from datetime import datetime, timedelta
from models import Transaction

def check_fraud(user_id, db, threshold=3):
    now = datetime.utcnow()
    window = now - timedelta(minutes=1)
    txns = Transaction.query.filter_by(sender_id=user_id).filter(Transaction.timestamp >= window).all()
    
    if len(txns) > threshold:
        for txn in txns:
            txn.flagged = True
        db.session.commit()
        return True
    return False
