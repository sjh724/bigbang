import datetime
from flask import request, render_template
from flask_login import login_required
from wtforms import Form, StringField, validators
from app.main.bigbang import LoginBruter
from app.models import Record
from . import main
from .. import db


@main.route('/admin')
@login_required
def for_admins_only():
    return "管理员"


@main.route('/moderator')
@login_required
def for_moderators_only():
    return "评论修改者"


@main.route('/user')
@login_required
def userinfo():
    return render_template('user.html')


class LoginForm(Form):
    host = StringField("host", [validators.data_required()])
    cache_translations = True


@main.route("/", methods=['GET'])
@login_required
def index():
    myForm = LoginForm(request.form)
    message = "请输入参数"
    return render_template('bigbang.html', message=message, form=myForm)


@main.route("/bigbang", methods=['GET', 'POST'])
def bigBang():
    myForm = LoginForm(request.form)
    print(request.method)
    username = ''
    password = ''
    statue = False
    if request.method == 'POST':
        message = "爆破失败"
        if myForm.host.data and myForm.validate():
            host = myForm.host.data
            ufile = "username.txt"
            pfile = "password.txt"
            login = LoginBruter(host,ufile,pfile)
            results = login.run()
            if results:
                username = results[0].get("username")
                password = results[0].get("password")
                message = "爆破成功"
                statue = True
        else:
            message = "type must be ssh or ftp or mysql"
    else:
        message = "请输入参数"
    record = Record(host=myForm.host.data,statue=statue)
    db.session.add(record)
    return render_template('sucess.html', message=message, username=username, password=password, form=myForm)

