from flask import Flask

def create_app(configuration):
    app = Flask(__name__)
    app.secret_key = configuration.SECRET
    app.config.from_object(configuration)
    app.config.from_pyfile('config.py')
    app.config["SQLALCHEMY_DATABASE_URI"]  = configuration.SQLALCHEMY_DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    configuration.APP = app

    @app.route('/')
    def index():
        return 'oi'
    
    @app.after_request
    def post_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*') #global access, to everyone(API case)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type') #
        response.headers.add('Access-Control-Allow-Methods',  'GET,PUT,POST,DELETE,OPTIONS') #
        return response

