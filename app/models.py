from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
###从flask_login导入UserMixin类
###USerMixin类包含的以上四种方法的默认实现。
from . import db, login_manager
###从程序的工厂函数引入login_manager实例
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
##导入生成令牌函数
from flask import current_app
from datetime import datetime


class Role_Url(db.Model):
    __tablename__ = 'roles_urls'
    id = db.Column(db.Integer, primary_key=True)
    rid = (db.String(64), db.ForeignKey('roles.id'))
    uid = (db.String(64), db.ForeignKey('urls.id'))

class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(64), unique=True, index=True)

    name = db.Column(db.String(64))
    
    password_hash = db.Column(db.String(128))

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)



    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

###很重要
@login_manager.user_loader
def load_user(user_uid):
    return User.query.get(int(user_uid))

