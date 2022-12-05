from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle



class FlaskTests(TestCase):


    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_setup(self):
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)
            self.assertIn('<h1>Boggle!</h1>',html)
            self.assertEqual(res.status_code,200)
            self.assertIn(b'<p>High Score:',res.data)
            self.assertIn(b'<p>Games Played:',res.data)
            self.assertIn(b'<p class="score">Score :',res.data)
            self.assertIn(b'<p class="timer">Time Left:',res.data)

    def test_true_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ['A','B','C','D','E'],
                    ['A','B','E','T','E'],
                    ['A','B','C','D','R'],
                    ['A','B','C','D','E'],
                    ['A','R','C','D','E']
                ]
        response = self.client.get('/guess-word?word=bet')
        self.assertEqual(response.json['result'], 'ok')
        res2 = client.get('/guess-word?word=bar')
        self.assertEqual(res2.json['result'],'ok')
        res3 = client.get('/guess-word?word=deer')
        self.assertEqual(res3.json['result'],'ok')


    def test_wrong_word(self):
        self.client.get('/')
        res = self.client.get('/guess-word?word=incorrect')
        self.assertEqual(res.json['result'],'not-on-board')



    # TODO -- write tests for every view function / feature!
