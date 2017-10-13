from shorturl import app
from flask import render_template,request,redirect
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField


class urlform(FlaskForm):

    longurl = StringField(validators=[InputRequired()])
    submit = SubmitField('create short url')


@app.route("/")
def index():
    #return index page
    form = urlform()
    return render_template('index.html', form=form)

@app.route("/<urlid>")
def backurl():
    #redirect url
    return "hey"