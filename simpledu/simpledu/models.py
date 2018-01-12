# 存放数据模型相关代码

from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
#flask 底层库提供了生成密码哈希的函数和检测密码哈希和密码是否相等的函数

db = SQLAlchemy()  # 此处不再传入 app,此处的 app 还没有进行定义

class Base(db.Model):
    """ 所有的 model 的一个基类，默认添加了时间戳 """
    __abstract__ = True  # 表示不要将这个类当作 Model 类

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 以上两个时间戳都不需要自己去维护


class User(Base, UserMixin):  # 继承 Base 类
    __tablename__ = 'user'
    """ 用数值表示角色，方便判断是否有权限，比如某个操作要角色为员工及以上那个用户才可以做，那么只要判断 user.role >= ROLE_STAFF,数值之间间隔10是为了方便加入其他角色"""
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)  # unique表示该值需要独一无二；index添加之后便于提高运行速度；nullableb表示该值不为空
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    # 默认情况下，sqlalchemy 会以字段名来定义列名，但这里是 _password,为私有字段，所以明确指定数据库列名为 password
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    job = db.Column(db.String(64))
    publish_courses = db.relationship('Course')

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):  # 该密码才是对外暴露的部分
        """ Python 风格的 getter """
        return self._password

    @password.setter
    def password(self, orig_password):
        """ Python 风格的 setter,这样设置 user.password 就会自动为 password 声称哈希值存入 _password 字段 """
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """ 判断用户输入的密码和存储的 hash 密码是否相等 """
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author = db.relationship('User', uselist=False)
