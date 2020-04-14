from flask import Flask, render_template, request, redirect, url_for
import csv
import data_manager
import time
from datetime import datetime
import database_manager

app = Flask(__name__, static_folder='static')

import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

app.config["IMAGE_UPLOADS"] = "/home/getulus/my_project/web/1st/ask-mate-remotemates/static"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG"]




def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/test")
def test_site():
    datas = database_manager.get_current_answer("1")
    return render_template("test.html", datas=datas)




@app.route("/")
def hello():

    return render_template("main.html")

@app.route('/list/', methods=["POST","GET"])
@app.route('/list', methods=["POST","GET"])
def list():
    if request.method == "POST":
        header =request.form["title"]
        if request.form["way"] == "Ascending":
            way = "ASC"
        else:
            way = "DESC"
        all_question_datas = database_manager.sort_questions(header, way)

        return render_template('list.html', all_q_data=all_question_datas)
    else:
        all_question_datas = database_manager.get_all_question()
        return render_template('list.html', all_q_data=all_question_datas)


@app.route("/list/question/<string:question_id>")
def display_question(question_id):

    current_q_data = database_manager.get_current_question(question_id)
    current_a_data = database_manager.get_current_answer(question_id)

    return render_template("display_question.html", id=question_id, current_a_data=current_a_data, current_q_data=current_q_data)


@app.route("/list/add-question", methods=["POST", "GET"])
def ask_question():
    time_stample = time.time()
    time_stample = datetime.fromtimestamp(time_stample)
    q_id = data_manager.create_id()
    if request.method == "POST":
        if request.form:
            database_manager.add_question(q_id, time_stample, request.form["title"], request.form["message"] )


        if request.files:
            return redirect(url_for("ask_question"))
        '''   
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
                database_manager.add_image(filename, )
                
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        '''

        return redirect(url_for("display_question", question_id=q_id))

    else:
        return render_template("add_question.html")


@app.route("/list/add-answer-image/<string:question_id>/<string:answer_id>", methods=["GET","POST"])
def upload_answer_image(question_id, answer_id):
    time_stample = time.time()
    time_stample = datetime.fromtimestamp(time_stample)
    if request.method == "POST":
        image = request.files["image"]
        if image.filename == "":
            print("image must have a filename")
            return redirect(request.url)
        if not allowed_image(image.filename):
            print("That image extension is not allowed")
            return redirect(request.url)
        else:
            filename = secure_filename(image.filename)
            database_manager.add_image("answer", filename, answer_id, time_stample)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        return redirect(url_for("display_question", question_id=question_id))



@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def new_answer(question_id):
    if request.method == "POST":
        time_stample = time.time()
        time_stample = datetime.fromtimestamp(time_stample)
        a_id = data_manager.create_id()
        database_manager.add_answer(question_id,a_id,time_stample,request.form["message"])

        return redirect(url_for("display_question", question_id=question_id))

    else:
        return render_template("new_answer.html")


@app.route("/question/<question_id>/edit", methods=["POST","GET"])
def edit_question(question_id):

    if request.method == "POST":
        time_stample = time.time()
        time_stample = datetime.fromtimestamp(time_stample)
        if request.form:
            database_manager.edit_question(request.form["title"], question_id, request.form["message"])

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
                database_manager.add_image("question", filename, question_id, time_stample)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

        return redirect(url_for("display_question", question_id=question_id))
    else:
        current_data = database_manager.get_current_question(question_id)
        return render_template("edit.html", current_data=current_data, question_id=question_id)




@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    database_manager.delete_question(question_id)
    return redirect(url_for("list"))

        

@app.route("/<question_id>/<answer_id>/delete")
def delete_answer(answer_id, question_id):

    database_manager.delete_answer(answer_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/question/<question_id>/vote_up")
def vote_up(question_id):
    database_manager.vote_question_up(question_id)
    return redirect(url_for("list"))


@app.route("/question/<question_id>/vote_down")
def vote_down(question_id):
    database_manager.vote_question_down(question_id)
    return redirect(url_for("list"))

@app.route("/<question_id>/answer/<answer_id>/vote_up")
def vote_a_up(answer_id, question_id):
    database_manager.vote_answer_up(answer_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/<question_id>/answer/<answer_id>/vote_down")
def vote_a_down(answer_id, question_id):
    database_manager.vote_answer_down(answer_id)
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
    data_manager.write_csv(all_q_data, 'sample_data/question.csv', data_manager.QUESTION_HEADERS)
    return redirect(url_for("list"))



if __name__ == "__main__":
    app.run(debug=True)

