from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from . import auth 
from ..models import User 
from .forms import LoginForm
from .forms import RegistrationForm
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index')) 

    return render_template('auth/login.html', form=form)


@auth.route('/logout') 
@login_required 
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,name=form.name.data,password=form.password.data)
        db.session.add(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)


       