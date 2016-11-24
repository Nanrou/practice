from flask_wtf import Form
from wtforms import TextField,BooleanField,PasswordField
from wtforms.validators import Required

class LoginFrom(Form):
    name = TextField('Name',validators=[Required()])
    password = PasswordField('password',validators=[Required()])
    remember_me = BooleanField('Remember_me',defluat = False)
    