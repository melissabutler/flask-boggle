from flask import Flask, request, render_template, session, jsonify, redirect

from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)

app.config['SECRET_KEY'] = "password"

app.debug = True

toolbar = DebugToolbarExtension(app)


# @app.route('/')
# def home_page():
#     """Shows home page"""
#     return render_template("home.html") 

# @app.route("/redirect")
# def redirect_start():
#     """Redirects to board upon clicking start button"""
#     return redirect("/board")


@app.route('/')
def board_page():
    """Shows home page and board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template("board.html", board=board, highscore=highscore, nplays=nplays)

@app.route('/check-word')
def check_word():
    """Checks validity of word"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    
    return jsonify({"result": response})

@app.route('/post-score', methods=["POST"])
def post_score():
    """Show number of games, final score for round, and increases number of games played"""
    score = request.json["score"]
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays',0)

    session['nplays']= nplays + 1
    session['highscore']= max(score, highscore)
    return jsonify(score)
