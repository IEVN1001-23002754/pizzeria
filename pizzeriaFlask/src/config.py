class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'julia02'
    MYSQL_PASSWORD = 'julia02'
    MYSQL_DB = 'pizzeria_julia'
    MYSQL_CURSORCLASS = 'Cursor'

config = { 'development': DevelopmentConfig }