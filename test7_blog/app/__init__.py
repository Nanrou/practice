from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


lm = LoginManager()
lm.setup_app(app)

from app import views,models