#coding:utf8

from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/1/')
def page1():
    return render_template('1.html')

if __name__ == '__main__':
    app.run(port=8000)