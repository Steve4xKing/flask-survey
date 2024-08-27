from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as primary_survey


app = Flask(__name__)


debug = DebugToolbarExtension(app)
# app.config for debugging
app.config['SECRET_KEY'] = 'whatever_my_secret_key_is' #this is a secret key that is used to encrypt the session cookie


responses = []
last_question_answered = 0


@app.route('/', methods=["GET","POST"])
def root():
    return render_template('index.html', survey=primary_survey)

@app.route('/questions/<int:question_id>', methods=["GET", "POST"])
def questions(question_id):
    if question_id != 0 and question_id != last_question_answered + 1:
        flash("Invalid question id", "error")
        return redirect(f'/questions/{last_question_answered}')
    return render_template('questions.html', survey=primary_survey, question_id=question_id)

@app.route('/questions/<int:question_id>/answer', methods=["GET", "POST"]) 
def next_question(question_id):
    global last_question_answered
    answer = request.form['choice']
    responses.append(answer)
    last_question_answered = question_id

    question_id += 1
    if question_id == len(primary_survey.questions):
        return redirect('/thanks')
    return redirect(f'/questions/{question_id}')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html', responses=responses)
