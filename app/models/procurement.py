import enum
from datetime import datetime, timezone

from app.extensions import db


class PRStatus(enum.Enum):
    draft = 'draft'
    submitted = 'submitted'
    approved = 'approved'
    rejected = 'rejected'


class POStatus(enum.Enum):
    draft = 'draft'
    sent = 'sent'
    confirmed = 'confirmed'
    received = 'received'
    closed = 'closed'
    cancelled = 'cancelled'


class RMLotStatus(enum.Enum):
    available = 'available'
    locked = 'locked'
    consumed = 'consumed'
    returned = 'returned'


class InvoiceMatchStatus(enum.Enum):
    pending = 'pending'
    matched = 'matched'
    exception = 'exception'


class PurchaseRequisition(db.Model):
    __tablename__ = 'purchase_requisitions'

    id = db.Column(db.Integer, primary_key=True)
    pr_number = db.Column(db.String(20), unique=True, nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    qty = db.Column(db.Numeric(12, 3), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.Enum(PRStatus), nullable=False, default=PRStatus.draft)
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    material = db.relationship('Material', backref='purchase_requisitions')
    requester = db.relationship('User', foreign_keys=[requested_by], backref='requisitions_made')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='requisitions_approved')
    purchase_orders = db.relationship('PurchaseOrder', backref='purchase_requisition', lazy='dynamic')


class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'

    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(20), unique=True, nullable=False)
    pr_id = db.Column(db.Integer, db.ForeignKey('purchase_requisitions.id'), nullable=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    qty_ordered = db.Column(db.Numeric(12, 3), nullable=False)
    unit_price = db.Column(db.Numeric(14, 2), nullable=False)
    total_amount = db.Column(db.Numeric(14, 2), nullable=False)
    expected_delivery_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum(POStatus), nullable=False, default=POStatus.draft)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    material = db.relationship('Material', backref='purchase_orders')
    creator = db.relationship('User', foreign_keys=[created_by], backref='purchase_orders_created')
    goods_receipts = db.relationship('GoodsReceipt', backref='purchase_order', lazy='dynamic')
    supplier_invoices = db.relationship('SupplierInvoice', backref='purchase_order', lazy='dynamic')


class GoodsReceipt(db.Model):
    __tablename__ = 'goods_receipts'

    id = db.Column(db.Integer, primary_key=True)
    gr_number = db.Column(db.String(20), unique=True, nullable=False)
    po_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)
    gross_weight = db.Column(db.Numeric(12, 3), nullable=False)
    tare_weight = db.Column(db.Numeric(12, 3), nullable=False)
    net_weight = db.Column(db.Numeric(12, 3), nullable=False)
    weight_variance_pct = db.Column(db.Numeric(6, 2), nullable=True)
    is_within_tolerance = db.Column(db.Boolean, nullable=True)
    received_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    received_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = db.Column(db.Text)

    receiver = db.relationship('User', foreign_keys=[received_by], backref='goods_receipts_received')
    rm_lots = db.relationship('RMLot', backref='goods_receipt', lazy='dynamic')


class RMLot(db.Model):
    __tablename__ = 'rm_lots'

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.String(25), unique=True, nullable=False)
    gr_id = db.Column(db.Integer, db.ForeignKey('goods_receipts.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    qty = db.Column(db.Numeric(12, 3), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Enum(RMLotStatus), nullable=False, default=RMLotStatus.available)
    putaway_location = db.Column(db.String(50), default='RM-WAREHOUSE')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    material = db.relationship('Material', backref='rm_lots')
    allocations = db.relationship('WOLotAllocation', backref='rm_lot', lazy='dynamic')


class SupplierInvoice(db.Model):
    __tablename__ = 'supplier_invoices'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), nullable=False)
    po_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    invoice_amount = db.Column(db.Numeric(14, 2), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    received_date = db.Column(db.Date, nullable=False)
    match_status = db.Column(db.Enum(InvoiceMatchStatus), nullable=False, default=InvoiceMatchStatus.pending)
    matched_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    creator = db.relationship('User', foreign_keys=[created_by], backref='supplier_invoices_created')
    payment_vouchers = db.relationship('PaymentVoucher', backref='supplier_invoice', lazy='dynamic')


class PaymentVoucher(db.Model):
    __tablename__ = 'payment_vouchers'

    id = db.Column(db.Integer, primary_key=True)
    voucher_number = db.Column(db.String(20), unique=True, nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('supplier_invoices.id'), nullable=False)
    amount = db.Column(db.Numeric(14, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    journal_entry = db.Column(db.JSON, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    paid_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    creator = db.relationship('User', foreign_keys=[created_by], backref='payment_vouchers_created')
