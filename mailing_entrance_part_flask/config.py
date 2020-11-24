import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/mailing"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '7a8fdb79ab334bad8bb17e9a4ccf9040'


class ProductConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
