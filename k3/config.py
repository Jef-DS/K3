class Config:
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///production.db'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'data.db'

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = ':memory:'