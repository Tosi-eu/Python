import os

class Configuration():
    CSRF_ENABLE = True
    SECRET = str(hash(os.getenv['USER']))
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None

class DevConfiguration(Configuration):
    DEBUG = True
    HOST_IP = "localhost"
    HOST_PORT = "8000"
    URL_MAIN = 'http:/%s/%s' % (HOST_IP, HOST_PORT)
    SQLALCHEMY_DB_URI = ''

class TestConfiguration(Configuration):
    DEBUG = True
    HOST_IP = "localhost"
    HOST_PORT = "8080"
    URL_MAIN = 'http://%s/%s' % (HOST_IP, HOST_PORT)
    SQLALCHEMY_DB_URI =  ''

class ProdConfiguration(Configuration):
    DEBUG = False
    HOST_IP = "localhost"
    HOST_PORT = "5000"
    URL_MAIN = 'http://%s/%s' % (HOST_IP, HOST_PORT)
    SQLALCHEMY_DB_URI = ''

app_config = {
    'development': DevConfiguration(),
    'testing': TestConfiguration(),
    'production': ProdConfiguration()
}

app_active = os.getenv('FLASK_STATE')

if app_active is None:
    app_active = 'development'
