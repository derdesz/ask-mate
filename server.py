from flask import Flask, render_template, request, redirect, url_for
import csv
import data_manager
import time
app = Flask(__name__, static_folder='static')

import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

app.config["IMAGE_UPLOADS"] = "/Users/derdesz/Desktop/projects/ask-mate-remotemates/static"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG"]

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/")
def hello():

    return render_template("main.html")

@app.route('/list', methods=["POST","GET"])
def list():
    if request.method == "POST":
        header =request.form["title"]
        if request.form["way"] == "Ascending":
            reversed = False
        else:
            reversed = True
        all_q_data = data_manager.read_sorted_csv('sample_data/question.csv', header, reversed)
        data_manager.write_csv(all_q_data, 'sample_data/question.csv',
                               ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"])
        return redirect(url_for("list"))
    else:
        all_question_datas = data_manager.read_csv('sample_data/question.csv')
        return render_template('list.html', rows=len(all_question_datas), all_data=all_question_datas)


@app.route("/list/question/<string:question_id>")
def display_question(question_id):
    all_q_data = data_manager.read_csv('sample_data/question.csv')
    all_a_data = data_manager.read_csv('sample_data/answer.csv')
    current_a_data = []
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i]["id"]:
            current_q_data = all_q_data[i]

    for i in range(len(all_a_data)):
        if question_id == all_a_data[i]["question_id"]:
            current_a_data.append(all_a_data[i])



    return render_template("display_question.html", id=question_id, current_a_data=current_a_data, current_q_data=current_q_data,
                           q_rows=len(data_manager.ALL_QUESTION_DATAS),
                           a_rows=len(data_manager.ALL_ANSWER_DATAS))


@app.route("/list/add-question", methods=["POST", "GET"])
def ask_question():
    time_stample = str(time.time())
    q_id = data_manager.create_id(data_manager.ALL_Q_ID)
    if request.method == "POST":
        if request.form:
            current_q_data = [q_id, time_stample, '0', '0', request.form["title"], request.form["message"], ' ']
            data_manager.add_element('sample_data/question.csv', current_q_data)
        if request.files:
            image = request.files["image"]
            filename = image.filename
            print(filename)
            if image.filename == "":
                print("image must have a filename")
                return redirect(request.url)
            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                current_q_data = [q_id, time_stample, '0', '0', '', '', filename]
                data_manager.add_element('sample_data/question.csv', current_q_data)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            return redirect(url_for("display_question", question_id=q_id))

        return redirect(url_for("display_question", question_id=q_id))

    else:
        return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def new_answer(question_id):
    if request.method == "POST":
        time_stample = str(time.time())
        a_id = data_manager.create_id(data_manager.ALL_A_ID)

        answer = [a_id, time_stample, "0", question_id, request.form["message"], " "]
        data_manager.add_element("sample_data/answer.csv", answer)
        return redirect(url_for("display_question", question_id=question_id))

    else:
        return render_template("new_answer.html")


@app.route("/question/<question_id>/edit", methods=["POST","GET"])
def edit_question(question_id):
    all_q_data = data_manager.read_csv('sample_data/question.csv')
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i]["id"]:
            current_data = all_q_data[i]
            index = i

    if request.method == "POST":
        time_stample = time.time()
        if request.form:
            all_q_data[index]["title"] = request.form["title"]
            all_q_data[index]["message"] = request.form["message"]
            all_q_data[index]["submission_time"] = time_stample
            data_manager.write_csv(all_q_data, 'sample_data/question.csv', ["id","submission_time","view_number","vote_number","title","message","image"])
        if request.files:
            image = request.files["image"]
            filename = image.filename
            if image.filename == "":
                print("image must have a filename")
                return redirect(request.url)
            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                all_q_data[index]["image"] = filename
                all_q_data[index]["submission_time"] = time_stample
                data_manager.write_csv(all_q_data, 'sample_data/question.csv',
                                       ["id", "submission_time", "view_number", "vote_number", "title", "message",
                                        "image"])
        return redirect(url_for("display_question", question_id=question_id))
    else:
        return render_template("edit.html", current_data=current_data, question_id=question_id)
        

@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    all_q_data = data_manager.read_csv('sample_data/question.csv')
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i]["id"]:
            all_q_data.remove(all_q_data[i])
            data_manager.write_csv(all_q_data, 'sample_data/question.csv', ["id","submission_time","view_number","vote_number","title","message","image"])
            return redirect(url_for("list"))

        

@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):

    all_a_data = data_manager.read_csv('sample_data/answer.csv')
    for i in range(len(all_a_data)):
        if answer_id == all_a_data[i]["id"]:
            question_id = all_a_data[i]["question_id"]
            all_a_data.remove(all_a_data[i])
            data_manager.write_csv(all_a_data, 'sample_data/answer.csv',
                                   ["id", "submission_time", "vote_number", "question_id", "message", "image"])
            return redirect(url_for("display_question", question_id=question_id))


@app.route("/question/<question_id>/vote_up")
def vote_up(question_id):
    all_q_data = data_manager.read_csv('sample_data/question.csv')
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i]["id"]:
            all_q_data[i]["vote_number"] = str(int(all_q_data[i]["vote_number"]) + 1)
            data_manager.write_csv(all_q_data, 'sample_data/question.csv', ["id","submission_time","view_number","vote_number","title","message","image"])
            return redirect(url_for("list"))


@app.route("/question/<question_id>/vote_down")
def vote_down(question_id):
    all_q_data = data_manager.read_csv('sample_data/question.csv')
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i]["id"]:
            all_q_data[i]["vote_number"] = str(int(all_q_data[i]["vote_number"]) - 1)
            data_manager.write_csv(all_q_data, 'sample_data/question.csv', ["id","submission_time","view_number","vote_number","title","message","image"])
            return redirect(url_for("list"))

@app.route("/answer/<answer_id>/vote_up")
def vote_a_up(answer_id):
    all_a_data = data_manager.read_csv('sample_data/answer.csv')
    for i in range(len(all_a_data)):
        if answer_id == all_a_data[i]["id"]:
            question_id = all_a_data[i]["question_id"]
            all_a_data[i]["vote_number"] = str(int(all_a_data[i]["vote_number"]) + 1)
            data_manager.write_csv(all_a_data, 'sample_data/answer.csv',
                                   ["id", "submission_time", "vote_number", "question_id", "message", "image"])
            return redirect(url_for("display_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote_down")
def vote_a_down(answer_id):
    all_a_data = data_manager.read_csv('sample_data/answer.csv')
    for i in range(len(all_a_data)):
        if answer_id == all_a_data[i]["id"]:
            question_id = all_a_data[i]["question_id"]
            all_a_data[i]["vote_number"] = str(int(all_a_data[i]["vote_number"]) - 1)
            data_manager.write_csv(all_a_data, 'sample_data/answer.csv',
                                   ["id", "submission_time", "vote_number", "question_id", "message", "image"])
            return redirect(url_for("display_question", question_id=question_id))

@app.route("/list/sort")
def sort():
    header = request.args["title"]
    reversed = request.args["order_direction"]
    if reversed == "descending":
        reversed = True
    else:
        reversed = False
    all_q_data = data_manager.read_sorted_csv('sample_data/question.csv', header, reversed)
    data_manager.write_csv(all_q_data, 'sample_data/question.csv', ["id","submission_time","view_number","vote_number","title","message","image"])
    return redirect(url_for("list"))



if __name__ == "__main__":
    app.run(debug=True)

