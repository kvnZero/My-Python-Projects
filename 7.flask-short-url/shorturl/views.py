from shorturl import app
from flask import render_template,request,redirect
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField
from shorturl.models import Urls, db


class urlform(FlaskForm):

    longurl = StringField(validators=[InputRequired()])
    submit = SubmitField('create short url')


@app.route("/",methods=['GET','POST'])
def index():
    form = urlform()
    if request.method == 'POST':
        long_url = form.longurl.data
        data = Urls.query.filter_by(url=long_url)
        if data.count() != 0:
            return render_template('index.html', title="create short url", form=form, shorturl=data.first().key)
        else:
            new_url = Urls(url=long_url, key="hello")
            db.session.add(new_url)
            db.session.commit()
            return render_template('index.html', title="create short url", form=form, shorturl=data.first().key)
    return render_template('index.html', title="create short url", form=form)

@app.route("/<urlkey>")
def backurl(urlkey):
    data = Urls.query.filter_by(key=urlkey)
    return redirect(data.first().url)