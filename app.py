from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Dipayan%40050519@localhost:3306/lilly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return redirect('/game')
    return render_template('index.html')
@app.route("/game", methods=['POST', 'GET'])
def game():
    word_list = Word.query.all()
    if not word_list:
        sample_words = ['VINICIUS', 'BELLINGHAM', 'NEYMAR', 'MESSI', 'RONALDO','MBAPPE','BRUNO','CUCURELLA','RODRYGO','IBRAHIMOVIC']
        for word in sample_words:
            new_word = Word(word=word)
            db.session.add(new_word)
        db.session.commit()
        word_list = Word.query.all()
    actual_word = random.choice(word_list).word.upper()
    display_word = '_' * len(actual_word)
    word_set = set(actual_word)
    flag = False
    guess = 6
    return render_template('game.html', actual_word=actual_word, display_word=display_word, word_set=word_set, flag=flag, guess=guess)


@app.route("/play", methods=['POST'])
def play():
    actual_word = request.form['actual_word']
    display_word = request.form['display_word']
    word_set = set(request.form['word_set'])
    guess = int(request.form['guess'])
    letter = request.form['letter'].upper()

    if letter in word_set:
        word_set.remove(letter)
        message = 'Right guess'
        display_word = ''.join([letter if actual_word[i] == letter else display_word[i] for i in range(len(actual_word))])

    else:
        guess -= 1
        message = 'Wrong guess'

    if '_' not in display_word:
        flag = True
        message = f'CONGRATS! YOU WON!! A MAN WILL LIVE TO SEE ANOTHER DAY THE WORD WAS --> {actual_word}'
    elif guess == 0:
        flag = True
        message = f'YOU LOST AND A MAN IS HANGED BECAUSE OF YOU!! THE RIGHT ANSWER WAS --> {actual_word}'
    else:
        flag = False

    return render_template('game.html', actual_word=actual_word, display_word=display_word, word_set=word_set, flag=flag, guess=guess, message=message)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)