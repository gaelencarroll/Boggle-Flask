from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iloveboggle'
boggle_game = Boggle()


@app.route('/')
def index():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore',0)
    games_played = session.get('games_played',0)
    return render_template('index.html', board=board, games_played=games_played, highscore=highscore)


@app.route('/guess-word')
def guess_word():
    board = session['board']
    word = request.args['word']
    res = boggle_game.check_valid_word(board, word)
    return jsonify({'result': res})

@app.route('/update-score',methods=['POST'])
def update_score():
    print('update-score')
    game_score = request.json['score']
    highscore = session.get('highscore',0)
    games_played = session.get('games_played',0)
    session['games_played'] = games_played + 1
    session['highscore'] = max(highscore,game_score)
    return jsonify(record=game_score > highscore)
