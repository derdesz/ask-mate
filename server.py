from flask import Flask, render_template
import csv
import data_manager
app = Flask(__name__)


@app.route("/")
def hello():

    return render_template("main.html")

@app.route('/list')
def list():

    question_list = []
    for rows in data_manager.ALL_QUESTION_DATAS:
        question_list.append(rows[5])

    return render_template('list.html', question_list=question_list, rows=len(question_list), cols=len(question_list[0]), id=id)

@app.route("/list/<question_id>")
def display_question(question_id):
    return render_template("display_question.html")




if __name__ == "__main__":
    app.run(debug=True)
