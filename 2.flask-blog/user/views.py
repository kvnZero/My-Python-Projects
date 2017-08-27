from user import app
from flask import render_template,request
from user.sqlite import Essay

@app.route('/')
@app.route('/page/<page>')
@app.route('/class/<essay_class>')
@app.route('/class/<essay_class>/page/<page>')
def index(page=1,essay_class='all'):
    essays = Essay.query.order_by(Essay.id.desc()).limit(5)
    phpamount = Essay.query.filter_by(essay_class='php').count()
    pythonamount = Essay.query.filter_by(essay_class='python').count()
    allamount = Essay.query.count()
    return render_template('index.html', 
                            Essays = essays,
                            allamount = allamount,
                            phpamount = phpamount,
                            pythonamount = pythonamount,
                            choose = essay_class )

@app.route('/essay/<essay_id>')
def essay(essay_id):
    essay = Essay.query.filter_by(id=essay_id).first()
    return render_template ('essay.html',essay = essay)