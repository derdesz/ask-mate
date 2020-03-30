from flask import Flask, render_template
import csv
import data_manager
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/list')
def list():
    question_list = data_manager.read_csv('sample_data/question.csv')
    return render_template('list.html', question_list=question_list)


if __name__ == "__main__":
    app.run(debug=True)
