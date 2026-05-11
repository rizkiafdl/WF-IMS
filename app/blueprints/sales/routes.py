from flask import render_template
from flask_login import login_required
from . import bp


@bp.route('/so')
@login_required
def so_list():
    return render_template('coming_soon.html', title='Sales Orders')


@bp.route('/delivery')
@login_required
def delivery_list():
    return render_template('coming_soon.html', title='Deliveries')


@bp.route('/invoice')
@login_required
def invoice_list():
    return render_template('coming_soon.html', title='Sales Invoices')


@bp.route('/payment')
@login_required
def payment_list():
    return render_template('coming_soon.html', title='Payments Received')
