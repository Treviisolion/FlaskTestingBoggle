from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    def test_make_board(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<table>\n    \n    <tr>\n        \n        <td>", html) # TODO: Find a better way to test that the board was made

    def test_check_word(self):
        with app.test_client() as client:
            with app.app_context():
                pass
            yield client

            # Setting board to be full of 'A's with a single 'THE' word to test for
            with client.session_transaction() as change_session:
                change_session["board"] = [['T', 'H', 'E', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], [
                    'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']]
            word = "testwordhi"

            resp = client.post('/api/submitword', data=jsonify({word}))
            data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, "not-word")

            word = "background"

            resp = client.post('/api/submitword', data=jsonify({word}))
            data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, "not-on-board")

            word = "the"

            resp = client.post('/api/submitword', data=jsonify({word}))
            data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, "ok")

    def test_game_over(self):
        with app.test_client() as client:
            with app.app_context():
                pass
            yield client

            # Testing initial gameover
            score = 50

            resp = client.post('/api/gameover', data=jsonify({score}))
            data = resp.get_dat(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data.highscore, 50)
            self.assertEqual(data.num_of_games, 1)

            with client.session_transaction() as change_session:
                change_session["games"] = 999

            # Testing gameover with no new highscore
            score = 4

            resp = client.post('/api/gameover', data=jsonify({score}))
            data = resp.get_dat(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data.highscore, 50)
            self.assertEqual(data.num_of_games, 1000)

            # Testing gameover with new highscore
            score = 51

            resp = client.post('/api/gameover', data=jsonify({score}))
            data = resp.get_dat(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data.highscore, 51)
            self.assertEqual(data.num_of_games, 1001)
