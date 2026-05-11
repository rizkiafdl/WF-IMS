from datetime import date, datetime, timezone

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.inventory import StockTransaction, TransactionType
from app.models.master import Material, Vendor
from app.models.procurement import (
    GoodsReceipt, InvoiceMatchStatus, PaymentVoucher, POStatus, PRStatus,
    PurchaseOrder, PurchaseRequisition, RMLot, RMLotStatus, SupplierInvoice,
)
from app.utils import gen_doc_number

from . import bp


def _parse_date(s):
    return date.fromisoformat(s) if s else None


# ─── Purchase Requisitions ────────────────────────────────────────────────────

@bp.route('/pr')
@login_required
def pr_list():
    prs = PurchaseRequisition.query.order_by(PurchaseRequisition.created_at.desc()).all()
    return render_template('procurement/pr_list.html', prs=prs)


@bp.route('/pr/new', methods=['GET', 'POST'])
@login_required
def pr_new():
    materials = Material.query.order_by(Material.name).all()
    if request.method == 'POST':
        pr = PurchaseRequisition(
            pr_number=gen_doc_number('PR', PurchaseRequisition, 'pr_number'),
            material_id=int(request.form['material_id']),
            qty=request.form['qty'],
            unit=request.form['unit'].strip(),
            reason=request.form.get('reason', '').strip() or None,
            status=PRStatus.draft,
            requested_by=current_user.id,
        )
        db.session.add(pr)
        db.session.commit()
        flash(f'PR {pr.pr_number} berhasil dibuat.', 'success')
        return redirect(url_for('procurement.pr_detail', pr_id=pr.id))
    return render_template('procurement/pr_form.html', materials=materials)


@bp.route('/pr/<int:pr_id>')
@login_required
def pr_detail(pr_id):
    pr = PurchaseRequisition.query.get_or_404(pr_id)
    return render_template('procurement/pr_detail.html', pr=pr)


@bp.route('/pr/<int:pr_id>/submit', methods=['POST'])
@login_required
def pr_submit(pr_id):
    pr = PurchaseRequisition.query.get_or_404(pr_id)
    if pr.status != PRStatus.draft:
        flash('PR tidak dalam status Draft.', 'error')
        return redirect(url_for('procurement.pr_detail', pr_id=pr_id))
    pr.status = PRStatus.submitted
    db.session.commit()
    flash(f'PR {pr.pr_number} berhasil disubmit.', 'success')
    return redirect(url_for('procurement.pr_detail', pr_id=pr_id))


@bp.route('/pr/<int:pr_id>/approve', methods=['POST'])
@login_required
def pr_approve(pr_id):
    pr = PurchaseRequisition.query.get_or_404(pr_id)
    if pr.status != PRStatus.submitted:
        flash('PR tidak dalam status Submitted.', 'error')
        return redirect(url_for('procurement.pr_detail', pr_id=pr_id))
    pr.status = PRStatus.approved
    pr.approved_by = current_user.id
    pr.approved_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(f'PR {pr.pr_number} disetujui.', 'success')
    return redirect(url_for('procurement.pr_detail', pr_id=pr_id))


@bp.route('/pr/<int:pr_id>/reject', methods=['POST'])
@login_required
def pr_reject(pr_id):
    pr = PurchaseRequisition.query.get_or_404(pr_id)
    if pr.status != PRStatus.submitted:
        flash('PR tidak dalam status Submitted.', 'error')
        return redirect(url_for('procurement.pr_detail', pr_id=pr_id))
    pr.status = PRStatus.rejected
    pr.approved_by = current_user.id
    pr.approved_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(f'PR {pr.pr_number} ditolak.', 'warning')
    return redirect(url_for('procurement.pr_detail', pr_id=pr_id))


# ─── Purchase Orders ──────────────────────────────────────────────────────────

@bp.route('/po')
@login_required
def po_list():
    pos = PurchaseOrder.query.order_by(PurchaseOrder.created_at.desc()).all()
    return render_template('procurement/po_list.html', pos=pos)


@bp.route('/po/new/<int:pr_id>', methods=['GET', 'POST'])
@login_required
def po_new(pr_id):
    pr = PurchaseRequisition.query.get_or_404(pr_id)
    vendors = Vendor.query.filter_by(is_active=True).order_by(Vendor.name).all()
    if request.method == 'POST':
        qty = float(request.form['qty_ordered'])
        unit_price = float(request.form['unit_price'])
        po = PurchaseOrder(
            po_number=gen_doc_number('PO', PurchaseOrder, 'po_number'),
            pr_id=pr.id,
            vendor_id=int(request.form['vendor_id']),
            material_id=pr.material_id,
            qty_ordered=qty,
            unit_price=unit_price,
            total_amount=round(qty * unit_price, 2),
            expected_delivery_date=_parse_date(request.form.get('expected_delivery_date', '')),
            status=POStatus.draft,
            created_by=current_user.id,
        )
        db.session.add(po)
        db.session.commit()
        flash(f'PO {po.po_number} berhasil dibuat.', 'success')
        return redirect(url_for('procurement.po_detail', po_id=po.id))
    return render_template('procurement/po_form.html', pr=pr, vendors=vendors)


@bp.route('/po/<int:po_id>')
@login_required
def po_detail(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    grs = po.goods_receipts.all()
    invoices = po.supplier_invoices.all()
    return render_template('procurement/po_detail.html', po=po, grs=grs, invoices=invoices)


@bp.route('/po/<int:po_id>/send', methods=['POST'])
@login_required
def po_send(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    if po.status != POStatus.draft:
        flash('PO tidak dalam status Draft.', 'error')
        return redirect(url_for('procurement.po_detail', po_id=po_id))
    po.status = POStatus.sent
    db.session.commit()
    flash(f'PO {po.po_number} berhasil dikirim ke vendor.', 'success')
    return redirect(url_for('procurement.po_detail', po_id=po_id))


@bp.route('/po/<int:po_id>/confirm', methods=['POST'])
@login_required
def po_confirm(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    if po.status != POStatus.sent:
        flash('PO tidak dalam status Sent.', 'error')
        return redirect(url_for('procurement.po_detail', po_id=po_id))
    po.status = POStatus.confirmed
    po.confirmed_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(f'PO {po.po_number} dikonfirmasi oleh vendor.', 'success')
    return redirect(url_for('procurement.po_detail', po_id=po_id))


# ─── Goods Receipts ───────────────────────────────────────────────────────────

@bp.route('/gr')
@login_required
def gr_list():
    grs = GoodsReceipt.query.order_by(GoodsReceipt.received_at.desc()).all()
    return render_template('procurement/gr_list.html', grs=grs)


@bp.route('/gr/new/<int:po_id>', methods=['GET', 'POST'])
@login_required
def gr_new(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    if po.status not in (POStatus.confirmed, POStatus.sent):
        flash('GR hanya bisa dibuat untuk PO Confirmed atau Sent.', 'error')
        return redirect(url_for('procurement.po_detail', po_id=po_id))
    if request.method == 'POST':
        gross = float(request.form['gross_weight'])
        tare = float(request.form['tare_weight'])
        net = round(gross - tare, 3)
        variance_pct = round((net - float(po.qty_ordered)) / float(po.qty_ordered) * 100, 2)
        within_tol = abs(variance_pct) <= 5.0

        gr = GoodsReceipt(
            gr_number=gen_doc_number('GR', GoodsReceipt, 'gr_number'),
            po_id=po.id,
            gross_weight=gross,
            tare_weight=tare,
            net_weight=net,
            weight_variance_pct=variance_pct,
            is_within_tolerance=within_tol,
            received_by=current_user.id,
            notes=request.form.get('notes', '').strip() or None,
        )
        db.session.add(gr)
        db.session.flush()

        lot = RMLot(
            lot_id=gen_doc_number('LOT', RMLot, 'lot_id'),
            gr_id=gr.id,
            material_id=po.material_id,
            qty=net,
            unit=po.material.unit,
            status=RMLotStatus.available,
            putaway_location=request.form.get('putaway_location', 'RM-WAREHOUSE').strip() or 'RM-WAREHOUSE',
        )
        db.session.add(lot)
        db.session.flush()

        db.session.add(StockTransaction(
            transaction_type=TransactionType.gr_in,
            material_id=po.material_id,
            lot_id=lot.lot_id,
            qty_change=net,
            reference_type='GoodsReceipt',
            reference_id=gr.id,
            notes=f'GR {gr.gr_number} — Lot {lot.lot_id}',
            created_by=current_user.id,
        ))

        po.status = POStatus.received
        db.session.commit()

        flash(f'GR {gr.gr_number} disimpan. Lot ID: {lot.lot_id}. '
              f'Variance: {variance_pct:+.2f}% '
              f'({"dalam" if within_tol else "di luar"} toleransi ±5%).', 'success')
        return redirect(url_for('procurement.po_detail', po_id=po_id))
    return render_template('procurement/gr_form.html', po=po)


# ─── Supplier Invoices ────────────────────────────────────────────────────────

@bp.route('/invoice')
@login_required
def invoice_list():
    invoices = SupplierInvoice.query.order_by(SupplierInvoice.created_at.desc()).all()
    return render_template('procurement/invoice_list.html', invoices=invoices)


@bp.route('/invoice/new/<int:po_id>', methods=['GET', 'POST'])
@login_required
def invoice_new(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    if request.method == 'POST':
        inv = SupplierInvoice(
            invoice_number=request.form['invoice_number'].strip(),
            po_id=po.id,
            vendor_id=po.vendor_id,
            invoice_amount=float(request.form['invoice_amount']),
            invoice_date=_parse_date(request.form['invoice_date']),
            received_date=_parse_date(request.form['received_date']),
            match_status=InvoiceMatchStatus.pending,
            created_by=current_user.id,
        )
        db.session.add(inv)
        db.session.commit()
        flash(f'Invoice {inv.invoice_number} berhasil disimpan.', 'success')
        return redirect(url_for('procurement.invoice_list'))
    return render_template('procurement/invoice_form.html', po=po)


@bp.route('/invoice/<int:invoice_id>/match', methods=['POST'])
@login_required
def invoice_match(invoice_id):
    inv = SupplierInvoice.query.get_or_404(invoice_id)
    po = inv.purchase_order
    gr = po.goods_receipts.order_by(GoodsReceipt.received_at.desc()).first()

    if not gr:
        flash('Belum ada GR untuk PO ini — tidak bisa 3-way match.', 'error')
        return redirect(url_for('procurement.invoice_list'))

    qty_var = abs((float(gr.net_weight) - float(po.qty_ordered)) / float(po.qty_ordered))
    price_var = abs((float(inv.invoice_amount) - float(po.total_amount)) / float(po.total_amount))

    if qty_var <= 0.02 and price_var <= 0.01:
        inv.match_status = InvoiceMatchStatus.matched
        msg = '3-Way Match berhasil — invoice matched.'
        cat = 'success'
    else:
        inv.match_status = InvoiceMatchStatus.exception
        msg = f'3-Way Match gagal — qty var {qty_var:.1%}, price var {price_var:.1%}. Exception queue.'
        cat = 'warning'

    inv.matched_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(msg, cat)
    return redirect(url_for('procurement.invoice_list'))


@bp.route('/invoice/<int:invoice_id>/pay', methods=['POST'])
@login_required
def invoice_pay(invoice_id):
    inv = SupplierInvoice.query.get_or_404(invoice_id)
    if inv.match_status != InvoiceMatchStatus.matched:
        flash('Invoice harus berstatus Matched sebelum bisa dibayar.', 'error')
        return redirect(url_for('procurement.invoice_list'))
    if inv.payment_vouchers.count() > 0:
        flash('Invoice sudah memiliki payment voucher.', 'error')
        return redirect(url_for('procurement.invoice_list'))

    pv = PaymentVoucher(
        voucher_number=gen_doc_number('PV', PaymentVoucher, 'voucher_number'),
        invoice_id=inv.id,
        amount=inv.invoice_amount,
        payment_method=request.form.get('payment_method', 'Bank Transfer'),
        payment_date=_parse_date(request.form['payment_date']),
        journal_entry={
            'debit': 'Accounts Payable',
            'credit': 'Bank',
            'amount': float(inv.invoice_amount),
        },
        created_by=current_user.id,
    )
    db.session.add(pv)
    db.session.commit()
    flash(f'Payment Voucher {pv.voucher_number} berhasil dibuat.', 'success')
    return redirect(url_for('procurement.payment_list'))


# ─── Payments ─────────────────────────────────────────────────────────────────

@bp.route('/payment')
@login_required
def payment_list():
    payments = PaymentVoucher.query.order_by(PaymentVoucher.paid_at.desc()).all()
    return render_template('procurement/payment_list.html', payments=payments)
