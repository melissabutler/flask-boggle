from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS']= ['dont-show-debug-toolbar']


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

    def test_session_info_set(self):
        """ Test session count in nplays"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['nplays'] = 999

                response = client.get('/')
                
                self.assertEqual(response.status_code, 200)
                self.assertEqual(session['nplays'], 1000)



# Check word responses, valid/invalid/nan
    def test_check_valid_word(self):
        """Test that a valid word will get the correct json response"""
        with app.test_client as client:
            # create a board pre-session to guarantee that tested word will result in ok:
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
        """ test that an word not on the board will respond with the proper json response"""
        with app.test_client as client:
            response = client.get('/check-word?word=improbable')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_check_not_a_word(self):
        """Test that a non-word will resp ond with the proper json response"""
        with app.test_client as client:
            response = client.get('/check-word?word=bleeuahgoogabooga')
            self.assertEqual(response.json['result'], 'not-word')