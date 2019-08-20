from flask_sqlalchemy import SQLAlchemy
from user import app
import os 
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class Essay(db.Model):
    __tablename__ = 'essay'

    id = db.Column(db.Integer, primary_key=True)
    essay_title = db.Column(db.String(128))
    essay_class = db.Column(db.String(64),default="other")
    essay_summary = db.Column(db.String(256),nullable=True)
    essay_content = db.Column(db.Text)
    essay_time = db.Column(db.String(64))
    def __repr__(self):
        return '<Essay %r>' % self.essay_title