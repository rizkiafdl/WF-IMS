from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.extensions import db
from app.models.master import BOMItem, Customer, Material, MaterialType, Vendor

from . import bp


# ─── Vendors ─────────────────────────────────────────────────────────────────

@bp.route('/vendors')
@login_required
def vendor_list():
    vendors = Vendor.query.order_by(Vendor.name).all()
    return render_template('master/vendors.html', vendors=vendors)


@bp.route('/vendors/new', methods=['GET', 'POST'])
@login_required
def vendor_new():
    if request.method == 'POST':
        v = Vendor(
            name=request.form['name'].strip(),
            contact_name=request.form.get('contact_name', '').strip() or None,
            phone=request.form.get('phone', '').strip() or None,
            email=request.form.get('email', '').strip() or None,
            address=request.form.get('address', '').strip() or None,
            payment_terms=int(request.form['payment_terms']) if request.form.get('payment_terms') else None,
        )
        db.session.add(v)
        db.session.commit()
        flash(f'Vendor "{v.name}" berhasil ditambahkan.', 'success')
        return redirect(url_for('master.vendor_list'))
    return render_template('master/vendor_form.html', vendor=None)


@bp.route('/vendors/<int:vendor_id>/edit', methods=['GET', 'POST'])
@login_required
def vendor_edit(vendor_id):
    v = Vendor.query.get_or_404(vendor_id)
    if request.method == 'POST':
        v.name = request.form['name'].strip()
        v.contact_name = request.form.get('contact_name', '').strip() or None
        v.phone = request.form.get('phone', '').strip() or None
        v.email = request.form.get('email', '').strip() or None
        v.address = request.form.get('address', '').strip() or None
        v.payment_terms = int(request.form['payment_terms']) if request.form.get('payment_terms') else None
        v.is_active = 'is_active' in request.form
        db.session.commit()
        flash(f'Vendor "{v.name}" berhasil diperbarui.', 'success')
        return redirect(url_for('master.vendor_list'))
    return render_template('master/vendor_form.html', vendor=v)


# ─── Customers ───────────────────────────────────────────────────────────────

@bp.route('/customers')
@login_required
def customer_list():
    customers = Customer.query.order_by(Customer.name).all()
    return render_template('master/customers.html', customers=customers)


@bp.route('/customers/new', methods=['GET', 'POST'])
@login_required
def customer_new():
    if request.method == 'POST':
        c = Customer(
            name=request.form['name'].strip(),
            contact_name=request.form.get('contact_name', '').strip() or None,
            phone=request.form.get('phone', '').strip() or None,
            email=request.form.get('email', '').strip() or None,
            address=request.form.get('address', '').strip() or None,
            payment_terms=int(request.form['payment_terms']) if request.form.get('payment_terms') else None,
        )
        db.session.add(c)
        db.session.commit()
        flash(f'Customer "{c.name}" berhasil ditambahkan.', 'success')
        return redirect(url_for('master.customer_list'))
    return render_template('master/customer_form.html', customer=None)


@bp.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def customer_edit(customer_id):
    c = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        c.name = request.form['name'].strip()
        c.contact_name = request.form.get('contact_name', '').strip() or None
        c.phone = request.form.get('phone', '').strip() or None
        c.email = request.form.get('email', '').strip() or None
        c.address = request.form.get('address', '').strip() or None
        c.payment_terms = int(request.form['payment_terms']) if request.form.get('payment_terms') else None
        c.is_active = 'is_active' in request.form
        db.session.commit()
        flash(f'Customer "{c.name}" berhasil diperbarui.', 'success')
        return redirect(url_for('master.customer_list'))
    return render_template('master/customer_form.html', customer=c)


# ─── Materials ────────────────────────────────────────────────────────────────

@bp.route('/materials')
@login_required
def material_list():
    materials = Material.query.order_by(Material.name).all()
    return render_template('master/materials.html', materials=materials)


@bp.route('/materials/new', methods=['GET', 'POST'])
@login_required
def material_new():
    if request.method == 'POST':
        m = Material(
            name=request.form['name'].strip(),
            unit=request.form['unit'].strip(),
            reorder_point=request.form.get('reorder_point') or 0,
            material_type=MaterialType[request.form['material_type']],
        )
        db.session.add(m)
        db.session.commit()
        flash(f'Material "{m.name}" berhasil ditambahkan.', 'success')
        return redirect(url_for('master.material_list'))
    return render_template('master/material_form.html', material=None,
                           material_types=MaterialType, raw_materials=[], bom_items=[])


@bp.route('/materials/<int:material_id>/edit', methods=['GET', 'POST'])
@login_required
def material_edit(material_id):
    m = Material.query.get_or_404(material_id)
    raw_materials = (
        Material.query
        .filter_by(material_type=MaterialType.raw_material)
        .filter(Material.id != material_id)
        .order_by(Material.name)
        .all()
    )
    if request.method == 'POST':
        m.name = request.form['name'].strip()
        m.unit = request.form['unit'].strip()
        m.reorder_point = request.form.get('reorder_point') or 0
        db.session.commit()
        flash(f'Material "{m.name}" berhasil diperbarui.', 'success')
        return redirect(url_for('master.material_list'))
    bom_items = m.bom_as_fg.all() if m.material_type == MaterialType.finished_goods else []
    return render_template('master/material_form.html', material=m,
                           material_types=MaterialType, raw_materials=raw_materials,
                           bom_items=bom_items)


@bp.route('/materials/<int:material_id>/bom/add', methods=['POST'])
@login_required
def bom_add(material_id):
    Material.query.get_or_404(material_id)
    rm_id = request.form.get('rm_material_id')
    qty = request.form.get('qty_per_unit')
    if not rm_id or not qty:
        flash('Pilih bahan baku dan masukkan qty.', 'error')
    else:
        existing = BOMItem.query.filter_by(
            fg_material_id=material_id, rm_material_id=int(rm_id)
        ).first()
        if existing:
            existing.qty_per_unit = qty
        else:
            db.session.add(BOMItem(
                fg_material_id=material_id,
                rm_material_id=int(rm_id),
                qty_per_unit=qty,
            ))
        db.session.commit()
        flash('BOM item ditambahkan.', 'success')
    return redirect(url_for('master.material_edit', material_id=material_id))


@bp.route('/materials/<int:material_id>/bom/<int:bom_id>/delete', methods=['POST'])
@login_required
def bom_delete(material_id, bom_id):
    item = BOMItem.query.get_or_404(bom_id)
    db.session.delete(item)
    db.session.commit()
    flash('BOM item dihapus.', 'success')
    return redirect(url_for('master.material_edit', material_id=material_id))
