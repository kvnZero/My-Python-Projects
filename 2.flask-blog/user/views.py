from user import app
from flask import render_template,request
from flask_wtf import Form
from wtforms import TextAreaField, SelectField
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from user.sqlite import Essay
import re

app.config['SECRET_KEY'] = "abigeater"
app.config['Admin_username'] = "abigeater"
app.config['Admin_password'] = "xusong"

class EssayForm(Form):
    essay_title =  StringField('文章标题', validators=[Required()])
    essay_summary = TextAreaField('文章摘要')
    essay_class = SelectField('文章分类', choices=[('other','不分类'),('python','python'),('php','php')])
    essay_content = TextAreaField('文章内容')
    submit = SubmitField('发布文章')

@app.template_filter('change_summary')
def change_summary(l):
    content = re.sub('(<img.+?>)', '[图片]',l)
    return content[0:63]

@app.route('/')
@app.route('/page/<page>/')
@app.route('/class/<essay_class>/')
@app.route('/class/<essay_class>/page/<page>/')
def index(page=1,essay_class='all'):
    phpamount = Essay.query.filter_by(essay_class='php').count()
    pythonamount = Essay.query.filter_by(essay_class='python').count()
    allamount = Essay.query.count()
    if essay_class == 'all':
        essays = Essay.query.order_by(Essay.id.desc()).paginate(int(page), 5, False).items
        page_number = int(allamount / 5)+1
    elif essay_class == 'php':
        essays = Essay.query.filter_by(essay_class='php').order_by(Essay.id.desc()).paginate(int(page), 5, False).items
        page_number = int(phpamount / 5)+1
    elif essay_class == 'python':
        page_number = int(pythonamount / 5)+1
        essays = Essay.query.filter_by(essay_class='python').order_by(Essay.id.desc()).paginate(int(page), 5, False).items        

    
    return render_template('index.html', 
                            Essays = essays,
                            allamount = allamount,
                            phpamount = phpamount,
                            pythonamount = pythonamount,
                            choose = essay_class,
                            page_number = range(page_number)
                            )

@app.route('/essay/<essay_id>')
def essay(essay_id):
    essay = Essay.query.filter_by(id=essay_id).first()
    return render_template ('essay.html',essay = essay)

@app.route('/admin/<username>/<password>/')
def admin(username,password):
    if username != app.config['Admin_username'] or password != app.config['Admin_password']:
        return "Error Get.!"
    else:
        return render_template('adminuse.html')

@app.route('/admin/<username>/<password>/pushessay/', methods=['GET', 'POST'])
def pushessay(username,password):
    if username != app.config['Admin_username'] or password != app.config['Admin_password']:
        return "Error Get.!"
    else:
        form = EssayForm()
        return_content = ""
        if form.essay_title.data != None:
            name = form.essay_title.data
        return render_template('pushessay.html',form = form, return_content = return_content)
