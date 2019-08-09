from flask import Blueprint, render_template, flash, redirect, url_for
from MyBlog.forms import LoginForm,RegisterForm
from flask_login import logout_user, login_required, login_user
from MyBlog.utils import redirect_back
from MyBlog.models import Admin
from flask_login import current_user
from MyBlog.extensions import db

login_my = Blueprint('login', __name__)


@login_my.route('/login', methods=['GET', 'POST'])
def login():
    # 如果已登录，重定向回到主页
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.filter(Admin.username == username).first()  # 返回查询的第一条记录
        if admin:
            if admin.validate_password(password):
                login_user(admin, remember)# 登入用户
                ls_message = "欢迎回来"
                if current_user.is_superadmin:
                    ls_message = ls_message+(",超级管理员:%s" % current_user.name)
                elif current_user.is_admin:
                    ls_message = ls_message+(",管理员:%s" % current_user.name)
                else:
                    ls_message = ls_message+(",用户:%s" % current_user.name)
                flash(ls_message, 'info')
                return redirect_back()
            flash("密码错误", 'warning')
        else:
            flash("用户名错误")
    return render_template('login/login.html', form=form)


@login_my.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功！', 'info')
    return redirect(url_for('blog.index'))


@login_my.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not Admin.query.filter_by(username=form.username.data).first() or not Admin.query.filter_by(name=form.name.data).first():
            admin = Admin(
                username=form.username.data,
                name=form.name.data,
                blog_sub_title=form.blog_sub_title.data,
                blog_title=form.blog_title.data,
            )
            admin.set_password(form.password.data)
            admin.set_password(form.superword.data)
            db.session.add(admin)
            db.session.commit()
            flash("注册成功", "success")
        else:
            flash("用户名或昵称已被占用", "info")
        return redirect_back()
    return render_template("login/register.html", form=form)