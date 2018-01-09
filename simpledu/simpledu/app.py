# Flask App 的配置，创建相关代码

from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course

def create_app(config):
    """ 可以根据传入的 config 名称，加载不同的配置 """
    app = Flask(__name__)
    app.config.from_boject(configs.get(config))
    db.init_app(app)  # SQLAlchemy 的初始化方式改为使用 init_app，使用此将 app 传入db

    @app.route('/')
    def index():
        courses = Course.query.all()
        return render_template('index.html', courses=courses)

    @app.route('admin')
    def admin_index():
        return 'admin'
    
    return app
