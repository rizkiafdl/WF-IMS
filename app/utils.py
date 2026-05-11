from datetime import date

from app.extensions import db


def gen_doc_number(prefix, model_class, field_name):
    today = date.today().strftime('%Y%m%d')
    prefix_today = f"{prefix}-{today}-"
    col = getattr(model_class, field_name)
    last = (
        db.session.query(col)
        .filter(col.like(f"{prefix_today}%"))
        .order_by(col.desc())
        .limit(1)
        .scalar()
    )
    seq = int(last.rsplit('-', 1)[-1]) + 1 if last else 1
    return f"{prefix_today}{seq:03d}"
