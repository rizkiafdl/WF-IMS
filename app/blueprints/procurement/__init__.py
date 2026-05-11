from flask import Blueprint

bp = Blueprint('procurement', __name__, url_prefix='/procurement')

from . import routes  # noqa: F401
