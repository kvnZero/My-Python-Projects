from . import app
from flask import render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired
from fans.WeiboClass import Weibo
weibo = Weibo()

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])
    code = StringField('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Code:', validators=[InputRequired()])
    submit = SubmitField('Login Weibo')


@app.route('/')
def index():
    form = LoginForm()
    return render_template('login.html',form = form)

@app.route('/ajax/getcode/<username>/')
def getcode(username):
    weibo.setuser(username,"")
    return weibo.checkCode()

@app.route('/getcode/')
def getcodeimg():
    try:
        result_text = weibo.getCode()
        response = app.make_response(result_text)
        response.headers['Content-Type'] = 'image/jpeg'
        return response
    except ValueError:
        return ""

