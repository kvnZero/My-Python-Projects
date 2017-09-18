from . import app
from flask import render_template,redirect
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

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    uid, alerttext = None, None
    if form.username.data != None and form.password.data != None:
        weibo.setuser(form.username.data, form.password.data)
        if form.code.data != "":
            weibo.setCode(form.code.data)
        uid = weibo.loginWeibo()
    form.username.data = ""
    form.password.data = ""
    form.code.data = ""
    if uid != None:
        if uid == 0:
            alerttext = "username, password or code is error"
            return render_template('login.html', form=form, alerttext=alerttext)
        else:
            return redirect("/getfans/")

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

@app.route('/getfans/')
def getfans():
    weibo.getFans()
    return redirect("/showfans/")

@app.route('/showfans/')
def showfans():
    return str(weibo.showFans())