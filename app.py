import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True # never True at operate mode; user can exectue code
SECRET_KEY = 'devKey'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__) # will find all UPPERCASE vars above
# app.config.from_envvar("FLASKER_SETTINGS", silent=True) can load envvar, silent prevents if envvar doesn't exits

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db(): # sqlite3 /tmp/flaskr.db < schema.sql
    with closing(connect_db()) as db: # continues connection
        with app.open_resource('schema.sql') as f: # can read resource file
            db.cursor().executescript(f.read()) # cursor can execute whole script
        db.commit() # db commit explicitly
'''
Now : python shell can import like:
from flaskr import init_db
init_db()
'''
@app.before_request
def before_request():
    g.db = connect_db() # g have only one info of one request, supports thread

@app.teardown_request # when excepts
def teardown_request(exception):
    g.db.close()

if __name__ == '__main__':
    app.run()



