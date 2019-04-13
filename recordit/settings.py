# -*- coding: utf-8 -*-

import os
import sys
from uuid import uuid4

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret key')

    UPLOAD_PATH = os.path.join(basedir, 'uploads')

    FILE_CACHE_PATH = os.path.join(basedir, 'cache')

    ADMIN_NUMBER = os.getenv('ADMIN_NUMBER')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.sendgrid.net')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # file size exceed to 17 Mb will return a 413 error response.
    MAX_CONTENT_LENGTH = 17 * 1024 * 1024

    LOCALES = ['zh_Hans_CN', 'en_US']
    BABEL_DEFAULT_LOCALE = LOCALES[0]

    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    SENDGRID_DEFAULT_FROM = MAIL_USERNAME
    SENDGRID_API_KEY = MAIL_PASSWORD

    CACHE_TYPE = 'simple'

    MANAGE_USER_PER_PAGE = 30
    MANAGE_COURSE_PER_PAGE = 5
    MANAGE_REPORT_PER_PAGE = 30
    MANAGE_RECORD_TABLE_PER_PAGE = 30
    TABLE_MAX_WORDS = 10

    FILE_CACHE_PATH = os.path.join(basedir, 'cache')
    SYSTEM_LOG_PATH = os.path.join(basedir, 'logs/recordit.log')


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    SECRET_KEY = os.getenv('SECRET_KEY', uuid4().hex)
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
