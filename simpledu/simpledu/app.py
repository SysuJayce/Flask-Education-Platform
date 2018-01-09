# Flask App 的配置，创建相关代码

from flask import Flask
from simpledu.config import configs
from simpledu.models import db

def register_blueprints(app):
    from .handlers import front,course,admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)

def create_app(config):
    """ App 工厂 """
    """ 可以根据传入的 config 名称，加载不同的配置 """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)  # SQLAlchemy 的初始化方式改为使用 init_app，使用此将 app 传入db
    register_blueprints(app)
    return app
