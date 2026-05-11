import sqlite3
from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine

from .extensions import db, login_manager, migrate


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_app(config_object=None):
    app = Flask(__name__, static_folder='../static')

    if config_object is None:
        from config import DevelopmentConfig
        config_object = DevelopmentConfig

    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from app import models  # noqa: F401

    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.dashboard import bp as dashboard_bp
    from app.blueprints.master import bp as master_bp
    from app.blueprints.procurement import bp as procurement_bp
    from app.blueprints.production import bp as production_bp
    from app.blueprints.sales import bp as sales_bp
    from app.blueprints.inventory import bp as inventory_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(master_bp)
    app.register_blueprint(procurement_bp)
    app.register_blueprint(production_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(inventory_bp)

    @app.cli.command('seed-admin')
    def seed_admin():
        from app.models.user import User, UserRole
        if User.query.count() == 0:
            u = User(email='admin@wfims.com', full_name='Admin User', role=UserRole.admin)
            u.set_password('admin123')
            db.session.add(u)
            db.session.commit()
            print('Admin created: admin@wfims.com / admin123')
        else:
            print('Users already exist — skipping.')

    return app
