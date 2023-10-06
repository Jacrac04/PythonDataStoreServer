#!/usr/bin/env python

import os
from dotenv import load_dotenv
load_dotenv()


# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class. Contains default configuration settings
    + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='A very terrible secret key.')


class DevelopmentConfig(Config):
    DEBUG = True
    DB_TYPE = 'SQLITE'
    DATABASE_URI = "dev.sqlite"
    ISOLATION_LEVEL = 'DEFERRED'


class TestingConfig(Config):
    TESTING = True
    DB_TYPE = 'SQLITE'
    DATABASE_URI = "test.sqlite"
    ISOLATION_LEVEL = 'DEFERRED'


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    
    # Database settings
    DB_TYPE = 'SQLITE'
    DATABASE_URI = "production.sqlite"
    ISOLATION_LEVEL = 'DEFERRED'
    
    W_SECRET = os.getenv('W_SECRET')
