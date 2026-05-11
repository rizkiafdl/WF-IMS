import enum
from datetime import datetime, timezone

from app.extensions import db


class WOStatus(enum.Enum):
    draft = 'draft'
    submitted = 'submitted'
    approved = 'approved'
    rejected = 'rejected'
    in_progress = 'in_progress'
    production_complete = 'production_complete'
    completed = 'completed'


class StageStatus(enum.Enum):
    pending = 'pending'
    done = 'done'


class FGBatchStatus(enum.Enum):
    available = 'available'
    reserved = 'reserved'
    shipped = 'shipped'
    consumed = 'consumed'


class WorkOrder(db.Model):
    __tablename__ = 'work_orders'

    id = db.Column(db.Integer, primary_key=True)
    wo_number = db.Column(db.String(20), unique=True, nullable=False)
    fg_material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    target_qty = db.Column(db.Numeric(12, 3), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Enum(WOStatus), nullable=False, default=WOStatus.draft)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    fg_material = db.relationship('Material', foreign_keys=[fg_material_id], backref='work_orders')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='work_orders_approved')
    creator = db.relationship('User', foreign_keys=[created_by], backref='work_orders_created')
    stages = db.relationship(
        'WOProductionStage', backref='work_order', lazy='dynamic',
        order_by='WOProductionStage.stage_number',
    )
    lot_allocations = db.relationship('WOLotAllocation', backref='work_order', lazy='dynamic')
    fg_batches = db.relationship('FGBatch', backref='work_order', lazy='dynamic')


class WOProductionStage(db.Model):
    __tablename__ = 'wo_production_stages'

    id = db.Column(db.Integer, primary_key=True)
    wo_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'), nullable=False)
    stage_number = db.Column(db.Integer, nullable=False)  # 1–6
    stage_name = db.Column(db.String(20), nullable=False)  # chipping|drying|pelleting|cooling|screening|packing
    status = db.Column(db.Enum(StageStatus), nullable=False, default=StageStatus.pending)
    done_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    done_at = db.Column(db.DateTime, nullable=True)

    worker = db.relationship('User', foreign_keys=[done_by], backref='stages_done')


class WOLotAllocation(db.Model):
    __tablename__ = 'wo_lot_allocations'

    id = db.Column(db.Integer, primary_key=True)
    wo_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'), nullable=False)
    rm_lot_id = db.Column(db.Integer, db.ForeignKey('rm_lots.id'), nullable=False)
    qty_allocated = db.Column(db.Numeric(12, 3), nullable=False)
    qty_consumed = db.Column(db.Numeric(12, 3), nullable=True)


class FGBatch(db.Model):
    __tablename__ = 'fg_batches'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(25), unique=True, nullable=False)
    wo_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    qty = db.Column(db.Numeric(12, 3), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Enum(FGBatchStatus), nullable=False, default=FGBatchStatus.available)
    produced_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    material = db.relationship('Material', foreign_keys=[material_id], backref='fg_batches')
    so_line_items = db.relationship('SOLineItem', backref='fg_batch', lazy='dynamic')
