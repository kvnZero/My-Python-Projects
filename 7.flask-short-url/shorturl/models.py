from flask_sqlalchemy import SQLAlchemy
from shorturl import app
import os 
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class Urls(db.Model):
    __tablename__ = 'urls'
    url = db.Column(db.String(256))
    key = db.Column(db.String(6), unique=True)
    time = db.Column(db.DateTime)