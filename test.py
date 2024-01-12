from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_page(self):
        """ Test response from page, test html as text, test information is retrieved"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertIn("<h1>Let's Play Boggle! </h1>", response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("nplays"))

# Check word responses, valid/invalid/nan
    def test_check_valid_word(self):
        with app.test_client as client:
            # create a board to guarantee that tested word will result in ok:
            with client.session_transaction as sess:
                sess['board'] = [["Y", "E", "S", "S", "S"],
                                 ["Y", "E", "S", "S", "S"],
                                 ["Y", "E", "S", "S", "S"],
                                 ["Y", "E", "S", "S", "S"],
                                 ["Y", "E", "S", "S", "S"]
                                 ]
            response = client.get('/check-word?word=yes')
            self.assertEqual(response.json['result'], 'ok')

    def test_check_invalid_word(self):
        with app.test_client as client:
            response = client.get('/check-word?word=improbable')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_check_not_a_word(self):
        with app.test_client as client:
            response = client.get('/check-word?word=bleeuahgoogabooga')
            self.assertEqual(response.json['result'], 'not-word')