from datetime import datetime

from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from flask_json import FlaskJSON, JsonError, json_response, as_json

import database
import models
from blueprint import simple_page
from database import db_session

# configuration
DATABASE = './tmp/flaskr.db'
DEBUG = True # never True at operate mode; user can exectue code
SECRET_KEY = 'devKey'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
json = FlaskJSON(app)

app.config.from_object(__name__) # will find all UPPERCASE vars above
# app.config.from_envvar("FLASKER_SETTINGS", silent=True) can load envvar, silent prevents if envvar doesn't exits


def init_db():
    return database.init_db()

'''
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db(): # sqlite3 /tmp/flaskr.db < schema.sql
    with closing(connect_db()) as db: # continues connection
        with app.open_resource('schema.sql') as f: # can read resource file
            db.cursor().executescript(f.read()) # cursor can execute whole script
        db.commit() # db commit explicitly
'''
'''
Now : python shell can import like:
from flaskr import init_db
init_db()

@app.before_request
def before_request():
    g.db = connect_db() # g have only one info of one request, supports thread

@app.teardown_request # when excepts
def teardown_request(exception):
    g.db.close()
'''


@app.route('/get_user', methods=['GET'])
@as_json
def get_user():
    userdata = request.get_json()
    return models.User.query.filter(models.User.name=='admin').first()


@app.route('/add_user', methods=['POST'])
def add_user():
    request.get('username')
    u = models.User('admin', 'admin@localhost')
    db_session.add(u)
    db_session.commit()


@app.route('/')
def show_entries():
    result = models.Entry.query.all()
    entries = [dict(title=entry.title, text=entry.text) for entry in result]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entry = models.Entry(request.form['title'], request.form['text'])
    db_session.add(entry)
    db_session.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invaid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invaid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged in', None) # doesn't check if user logged in
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/get_time')
def get_time():
    now = datetime.utcnow()
    return json_response(time=now)


@app.route('/increment_value', methods=['POST'])
def increment_value():
    data = request.get_json(force=True) # skim mimetype, have shorte curl command
    try:
        value = int(data['value'])
    except (KeyError,TypeError, ValueError):
        raise JsonError(description='Invalid value.')
    return json_response(value=value+1)


@app.route('/get_value')
@as_json
def get_value():
    return dict(value=12)

app.register_blueprint(simple_page, url_prefix='/pages')


def get_blueprint_resource():
    with simple_page.open_resource('static/style.css') as f:
        code = f.read()

    from blueprint import Blueprint
    admin = Blueprint('admin', __name__
                      , static_folder='static'
                      , template_folder='templates')
    url_for('admin.static', filename='style.css')
    # /admin/admin.py blueprint,
    # ./index.html
    # ./templates/admin/index.html


if __name__ == '__main__':
    app.run()



