from flask import render_template
from flask_login import login_required
from sqlalchemy import func

from app.extensions import db
from app.models.inventory import StockTransaction
from app.models.master import Material
from app.models.procurement import POStatus, PurchaseOrder
from app.models.production import WOStatus, WorkOrder
from app.models.sales import SOStatus, SalesOrder

from . import bp


@bp.route('/')
@login_required
def index():
    open_po = PurchaseOrder.query.filter(
        PurchaseOrder.status.in_([POStatus.draft, POStatus.sent, POStatus.confirmed])
    ).count()

    active_wo = WorkOrder.query.filter(
        WorkOrder.status.in_([WOStatus.approved, WOStatus.in_progress])
    ).count()

    open_so = SalesOrder.query.filter(
        SalesOrder.status.in_([SOStatus.submitted, SOStatus.approved, SOStatus.picking])
    ).count()

    stock_sub = (
        db.session.query(
            StockTransaction.material_id,
            func.sum(StockTransaction.qty_change).label('balance'),
        )
        .group_by(StockTransaction.material_id)
        .subquery()
    )
    low_stock_count = (
        db.session.query(Material)
        .outerjoin(stock_sub, Material.id == stock_sub.c.material_id)
        .filter(
            db.or_(
                stock_sub.c.balance.is_(None),
                stock_sub.c.balance < Material.reorder_point,
            )
        )
        .count()
    )

    return render_template(
        'dashboard/index.html',
        open_po=open_po,
        active_wo=active_wo,
        open_so=open_so,
        low_stock_count=low_stock_count,
    )
