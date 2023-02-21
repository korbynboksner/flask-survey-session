from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "s"

R_K='responses'
@app.route("/")
def start():
    return render_template("start.html", survey = satisfaction_survey)

@app.route("/setup", methods=["POST"])
def set_up():
    session[R_K]=[]
    return redirect("/questions/0")

@app.route("/a", methods =["POST"])
def answer():
    c = request.form['answer']
    r = session[R_K]
    r.append(c)
    session[R_K] = r
    if len(satisfaction_survey.questions) == (len(r)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(r)}")

@app.route("/questions/<int:id>")
def q(id):
    r = session.get(R_K)

    if r == None:
        redirect("/")
    if len(satisfaction_survey.questions) == len(r):
        return redirect("/complete")
    if (len(r) != id):
        return redirect(f"/questions/{len(r)}")
    question = satisfaction_survey.questions[id]
   
    return render_template("questions.html", q=question, id=id)

@app.route("/complete")
def done():
    return render_template("done.html")