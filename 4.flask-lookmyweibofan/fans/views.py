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
    else:
        return render_template('login.html', form=form, alerttext=alerttext)

@app.route('/ajax/getcode/<username>/')
def getcode(username):
    if(len(str(username))<6):
        return "0"
    weibo.setuser(username,"")
    return weibo.checkCode()

@app.route('/getcode/<random>')
def getcodeimg(random=0):
    try:
        result_text = weibo.getCode()
        response = app.make_response(result_text)
        response.headers['Content-Type'] = 'image/jpeg'
        return response
    except ValueError:
        return ""

@app.route('/getfans/')
def getfans():
    try:
        weibo.getFans()
        return redirect("/showfans/")
    except ValueError:
        return "login after get fans.<br><a href='/'>return in index</a>"

@app.route('/showfans/')
def showfans():
    user = ""
    list = weibo.showFans()
    for i in list:
        str_i = list[i]
        user += "用户昵称：%s\t用户ID：%s\t关注：%s\t粉丝：%s\t微博：%s\t地址：%s\t关注来源：%s\n<br>" % (str_i[0],str_i[1],str_i[2],str_i[3],str_i[4],str_i[5],str_i[6])

    return str(user)