from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

boggle_game = Boggle()


@app.route('/')
def make_board():
    """Produces the board and creates main page"""

    session["board"] = boggle_game.make_board()
    return render_template('board.html', board=session["board"])


@app.route('/api/submitword', methods=['POST'])
def check_word():
    """Takes the word and checks if its valid then sends the response"""

    word = request.get_json().get("word")
    result = boggle_game.check_valid_word(session.get("board"), word)
    return jsonify(result)


@app.route('/api/gameover', methods=['POST'])
def game_over():
    """Takes the score provided, compares it with the highscore, then increments the number of games and returns that information"""

    score = request.get_json().get("score")
    if session.get("score", 0) < score:
        session["score"] = score
    session["games"] = session.get("games", 0) + 1
    return jsonify(highscore=session["score"], num_of_games=session["games"])
