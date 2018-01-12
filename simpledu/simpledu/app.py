# Flask App 的配置，创建相关代码

from flask_login import LoginManager
from flask import Flask
from simpledu.config import configs
from simpledu.models import db, User
from flask_migrate import Migrate

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)  # 将 LoginManager 注册到 app 和 数据库,即初始化 app

    @login_manager.user_loader  # 用 user_loader 装饰器注册一个函数，以加载用户对象
    def user_loader(id):
        return user.query.get(id)

    login_manager.login_view = 'front.login'  # login_view 设置的是登录页面的路由，有了它，当用 flask-login 提供的 login_required 装时期保护一个路由，如果用户未登录，那么就被重定向 login_view 页面

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
    register_extensions(app)
    register_blueprints(app)

    return app
