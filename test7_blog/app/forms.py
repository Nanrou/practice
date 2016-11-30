from flask_wtf import FlaskForm
from wtforms import TextField,BooleanField,PasswordField,TextAreaField,SubmitField
from wtforms.validators import Required,Email,Length

class LoginForm(FlaskForm):
    user_name = TextField('user name', validators=[Required(),Length(max=15)])
    remember_me = BooleanField('Remember_me', default=False)
    submit = SubmitField('Log in')
    
class SignUpForm(FlaskForm):
    user_name = TextAreaField('user name',validators=[Required(),Length(max=15)])
    user_email = TextAreaField('user email',validators=[Email(),Required(),Length(max=128)])
    submit = SubmitField('Sign up')

class AboutMeForm(FlaskForm):
    describe = TextAreaField('about me',validators=[Required(),Length(max=140)])
    submit = SubmitField('Yes!')
    
class PublishBlogForm(FlaskForm):
    body = TextAreaField('blog content',validators=[Required()])
    submit = SubmitField('Submit')