import enum
from datetime import datetime, timezone

from app.extensions import db


class SOStatus(enum.Enum):
    draft = 'draft'
    submitted = 'submitted'
    approved = 'approved'
    rejected = 'rejected'
    picking = 'picking'
    shipped = 'shipped'
    delivered = 'delivered'
    invoiced = 'invoiced'
    paid = 'paid'
    cancelled = 'cancelled'


class DOStatus(enum.Enum):
    pending = 'pending'
    shipped = 'shipped'
    delivered = 'delivered'


class SalesInvoiceStatus(enum.Enum):
    draft = 'draft'
    sent = 'sent'
    paid = 'paid'
    overdue = 'overdue'


class SalesOrder(db.Model):
    __tablename__ = 'sales_orders'

    id = db.Column(db.Integer, primary_key=True)
    so_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    status = db.Column(db.Enum(SOStatus), nullable=False, default=SOStatus.draft)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = db.Column(db.Text)

    approver = db.relationship('User', foreign_keys=[approved_by], backref='sales_orders_approved')
    creator = db.relationship('User', foreign_keys=[created_by], backref='sales_orders_created')
    line_items = db.relationship('SOLineItem', backref='sales_order', lazy='dynamic')
    delivery_orders = db.relationship('DeliveryOrder', backref='sales_order', lazy='dynamic')
    invoices = db.relationship('SalesInvoice', backref='sales_order', lazy='dynamic')


class SOLineItem(db.Model):
    __tablename__ = 'so_line_items'

    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    qty_ordered = db.Column(db.Numeric(12, 3), nullable=False)
    unit_price = db.Column(db.Numeric(14, 2), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('fg_batches.id'), nullable=True)
    qty_picked = db.Column(db.Numeric(12, 3), nullable=True)

    material = db.relationship('Material', foreign_keys=[material_id], backref='so_line_items')


class DeliveryOrder(db.Model):
    __tablename__ = 'delivery_orders'

    id = db.Column(db.Integer, primary_key=True)
    do_number = db.Column(db.String(20), unique=True, nullable=False)
    so_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'), nullable=False)
    driver_name = db.Column(db.String(100), nullable=False)
    vehicle_plate = db.Column(db.String(20), nullable=False)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(DOStatus), nullable=False, default=DOStatus.pending)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    creator = db.relationship('User', foreign_keys=[created_by], backref='delivery_orders_created')


class SalesInvoice(db.Model):
    __tablename__ = 'sales_invoices'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    so_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    amount = db.Column(db.Numeric(14, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum(SalesInvoiceStatus), nullable=False, default=SalesInvoiceStatus.draft)
    journal_entry = db.Column(db.JSON, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    paid_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    creator = db.relationship('User', foreign_keys=[created_by], backref='sales_invoices_created')
    receipt_vouchers = db.relationship('ReceiptVoucher', backref='sales_invoice', lazy='dynamic')


class ReceiptVoucher(db.Model):
    __tablename__ = 'receipt_vouchers'

    id = db.Column(db.Integer, primary_key=True)
    voucher_number = db.Column(db.String(20), unique=True, nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('sales_invoices.id'), nullable=False)
    amount = db.Column(db.Numeric(14, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    journal_entry = db.Column(db.JSON, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    creator = db.relationship('User', foreign_keys=[created_by], backref='receipt_vouchers_created')
