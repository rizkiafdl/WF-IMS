import os


class DevelopmentConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///wfims.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
