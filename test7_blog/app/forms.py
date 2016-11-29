from flask_wtf import Form
from wtforms import TextField,BooleanField,PasswordField,TextAreaField,SubmitField
from wtforms.validators import Required,Email,Length

class LoginForm(Form):
    user_name = TextField('user name', validators=[Required(),Length(max=15)])
    remember_me = BooleanField('Remember_me', default=False)
    submit = SubmitField('Log in')
    
class SignUpForm(Form):
    user_name = TextAreaField('user name',validators=[Required(),Length(max=15)])
    user_email = TextAreaField('user email',validators=[Email(),Required(),Length(max=128)])
    submit = SubmitField('Sign up')
    