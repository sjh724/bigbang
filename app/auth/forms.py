from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField

from wtforms.validators import Required, Length, Email,Regexp,EqualTo
from wtforms import ValidationError

from ..models import User



class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    
    password = PasswordField('密码', validators=[Required()]) 
    
    remember_me = BooleanField('记住密码')
    #
    submit = SubmitField('登录')


class RegistrationForm(Form):
	
	email = StringField('Email',validators=[Required(),Length(1,64),Email()])
	
	name = StringField('用户名',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',\
		0,'Usernames must have only letter,numbers,dots or underscores')])
	
	password = PasswordField('密码',validators=[Required(),EqualTo('password2',message='两次密码必须一致.')])
	
	password2 = PasswordField('确认密码',validators=[Required()])

	
	
	submit = SubmitField('注册')
	
	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email 已注册过.')

	
	def validata_name(self,field):
		if User.query.filter_by(name=field.data).first():
			raise ValidationError('用户名已存在.')