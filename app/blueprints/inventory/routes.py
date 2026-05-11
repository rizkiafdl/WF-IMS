from flask import render_template
from flask_login import login_required
from . import bp


@bp.route('/stock')
@login_required
def stock():
    return render_template('coming_soon.html', title='Stock Ledger')
