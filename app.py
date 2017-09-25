import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True # never True at operate mode; user can exectue code
SECRET_KEY = 'devKey'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__) # will find all UPPERCASE vars above
#app.config.from_envvar("FLASKER_SETTINGS", silent=True) can load envvar, silent prevents if envvar doesn't exits

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()



