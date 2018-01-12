from flask import Blueprint, render_template, flash, redirect, url_for
from simpledu.models import Course, User
from simpledu.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required


front = Blueprint('front', __name__)
# 省略了 url_prefix，那么默认就是 '/'

@front.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/logout')
@login_required  # 用 login_required 装饰器保护了这个路由器处理函数，未登录状态下访问这个页面会被重定向到登录页面
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))

@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # validate_on_submit 是 flask_wtf 提供的 FlaskForm 中封装的一个方法，返回是一个布尔值
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))  # .login 是 front.login 的简写，重定向到当前 Blueprint 下的某个路由就可以这样简写
    return render_template('register.html', form=form)

