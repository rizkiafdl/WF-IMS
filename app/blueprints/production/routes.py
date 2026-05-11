from flask import render_template
from flask_login import login_required
from . import bp


@bp.route('/wo')
@login_required
def wo_list():
    return render_template('coming_soon.html', title='Work Orders')
