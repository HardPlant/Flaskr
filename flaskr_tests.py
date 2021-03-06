import os
import tempfile
import unittest

from flask_json import JsonTestResponse

import flaskr


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        flaskr.app.response_class = JsonTestResponse
        self.app = flaskr.app.test_client()

        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirect=True)

    def test_messages(self):
        self.login('admin','default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here!?'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

    def test_time(self):
        rv = self.app.get('/get_time')
        assert '"status": 200' in rv.data
        assert '"time": ' in rv.data

    def test_get_value(self):
        rv = self.app.get('/get_value')
        assert '"value": 12' in rv.data

    def test_invalid_data(self):
        rv = self.app.post('/increment_value', data=dict(
            data='bla'
        ))
        assert '"status": 400' in rv.data
        assert '"description": "Not a JSON."' in rv.data

    def test_json(self):
        rv = self.app.get('/get_value')

        assert 'value' in rv.json
        assert type(rv.json['value']) is int



if __name__ == '__main__':
    unittest.main()