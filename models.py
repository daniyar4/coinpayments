from app import db
from datetime import datetime


class SavingTransactions(db.Model):
    """Make BD"""

    id = db.Column(db.Integer, primary_key=True)
    ipn_version = db.Column(db.Float)
    ipn_mode = db.Column(db.String(140))
    merchant_id = db.Column(db.String(140))
    txn_id = db.Column(db.String(140), unique=True)
    status = db.Column(db.Integer)
    email = db.Column(db.String(140))
    status_text = db.Column(db.String(140))
    currency2 = db.Column(db.String(70))
    amount2 = db.Column(db.Float)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(SavingTransactions, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Transaction %r>' % self.id
