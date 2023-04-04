from flask import Flask, request, render_template, redirect, flash
import surveys
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

Responses = list()



@app.route('/')
def home_page():
    """ this is the home page"""

    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions

    return render_template("app.html", title = title, instructions = instructions)

@app.route('/question/<int:num>')
def survey_questions(num):
    question_num = num

    if num == len(Responses):
        try:
            question = surveys.satisfaction_survey.questions[num].question
        except:
            return redirect('/thanks')
    else:
        flash("You are trying to access an invalid question")
        return redirect(f'/question/{len(Responses)}')

    choices = surveys.satisfaction_survey.questions[num].choices

    return render_template("questions.html",question = question,question_num = question_num,
                           choices = choices)

@app.route('/question/<int:num>',methods = ["POST"])
def save_answer(num):
    answer = request.form["answer"]
    Responses.append(answer)
    return redirect(f'/question/{num}')

    
@app.route('/thanks')
def thank_you():
    return render_template("thanks.html")

