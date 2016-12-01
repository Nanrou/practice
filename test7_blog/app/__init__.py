#coding:utf8
'''
整个包的头部
'''
from flask import Flask #导入flask
from flask_sqlalchemy import SQLAlchemy #导入flask-sql的接口
from flask_login import LoginManager #导入flask-login 这是封装了登陆的包

app = Flask(__name__)#将app定义为flask类
app.config.from_object('config')#导入config的配置

db = SQLAlchemy(app)#创建flask的数据库（sqlite3）

lm = LoginManager()#作为登陆的类
lm.setup_app(app)#

from app import views,models#从本类中导入views，models