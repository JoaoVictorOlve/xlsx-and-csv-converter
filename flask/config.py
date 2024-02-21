class Config(object):
    TESTING = False

    SECRET_KEY = "dasod234234fsda"

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = True

