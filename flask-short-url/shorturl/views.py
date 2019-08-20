from shorturl import app
from flask import render_template,request,redirect
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField
from shorturl.models import Urls, db
import random

class urlform(FlaskForm):
    longurl = StringField(validators=[InputRequired()])
    submit = SubmitField('create short url')

def randomkey():
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    a = list(chars)
    random.shuffle(a)
    return ''.join(a[:6])

@app.route("/",methods=['GET','POST'])
def index():
    form = urlform()
    if request.method == 'POST':
        long_url = form.longurl.data
        data = Urls.query.filter_by(url=long_url)
        if data.count() != 0:
            return render_template('index.html', title="create short url", form=form, urlkey=data.first().key)
        else:
            key = randomkey()
            keycount = Urls.query.filter_by(key=key).count()
            while keycount != 0:
                key = randomkey()
                keycount = Urls.query.filter_by(key=key).count()
            new_url = Urls(url=long_url, key=key)
            db.session.add(new_url)
            db.session.commit()
            return render_template('index.html', title="create short url", form=form, urlkey=data.first().key)
    return render_template('index.html', title="create short url", form=form)

@app.route("/s/<urlkey>")
def backurl(urlkey):
    data = Urls.query.filter_by(key=urlkey)
    return redirect(data.first().url)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')