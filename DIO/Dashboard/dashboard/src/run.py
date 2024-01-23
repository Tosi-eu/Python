from config import app_config, app_active
from app import create_app

config = app_config[app_active]

if __name__ == '__main__':
    create_app(config)
    config.APP.run(host=config.HOST_IP, port=config.HOST_PORT)