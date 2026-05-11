import enum
from datetime import datetime, timezone

from app.extensions import db


class TransactionType(enum.Enum):
    gr_in = 'gr_in'
    wo_consume = 'wo_consume'
    wo_produce = 'wo_produce'
    so_ship = 'so_ship'
    adjustment = 'adjustment'


class StockTransaction(db.Model):
    __tablename__ = 'stock_transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    lot_id = db.Column(db.String(25), nullable=True)  # rm lot_id or fg batch_id string
    qty_change = db.Column(db.Numeric(12, 3), nullable=False)  # positive=IN, negative=OUT
    reference_type = db.Column(db.String(50), nullable=True)  # GoodsReceipt|WorkOrder|SalesOrder
    reference_id = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    material = db.relationship('Material', foreign_keys=[material_id], backref='stock_transactions')
    creator = db.relationship('User', foreign_keys=[created_by], backref='stock_transactions_created')
