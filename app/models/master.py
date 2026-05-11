import enum
from datetime import datetime, timezone

from app.extensions import db


class MaterialType(enum.Enum):
    raw_material = 'raw_material'
    finished_goods = 'finished_goods'


class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    payment_terms = db.Column(db.Integer)  # days
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    purchase_orders = db.relationship('PurchaseOrder', backref='vendor', lazy='dynamic')
    supplier_invoices = db.relationship('SupplierInvoice', backref='vendor', lazy='dynamic')


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    payment_terms = db.Column(db.Integer)  # days
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    sales_orders = db.relationship('SalesOrder', backref='customer', lazy='dynamic')
    sales_invoices = db.relationship('SalesInvoice', backref='customer', lazy='dynamic')


class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(10), nullable=False)  # kg|ton|bag
    reorder_point = db.Column(db.Numeric(12, 3), default=0)
    material_type = db.Column(db.Enum(MaterialType), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    bom_as_fg = db.relationship(
        'BOMItem', foreign_keys='BOMItem.fg_material_id',
        backref='fg_material', lazy='dynamic',
    )
    bom_as_rm = db.relationship(
        'BOMItem', foreign_keys='BOMItem.rm_material_id',
        backref='rm_material', lazy='dynamic',
    )


class BOMItem(db.Model):
    __tablename__ = 'bom_items'

    id = db.Column(db.Integer, primary_key=True)
    fg_material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    rm_material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    qty_per_unit = db.Column(db.Numeric(12, 3), nullable=False)
