from user import app
from flask_script import Manager
from flaskext.markdown import Markdown
manager = Manager(app)
Markdown(app)
if __name__ == '__main__':
    app.run(debug=True)
    #manager.run()