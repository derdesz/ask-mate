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

app.config["IMAGE_UPLOADS"] = "/home/derdesz/Desktop/projects/ask-mate-remotemates/static"
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


@app.route("/", methods=["POST", "GET"])
def hello():
    if request.method == "POST":
        searched_word = request.form["search"]
        return redirect(url_for("search_question", search_phrase=searched_word))
    else:
        last_5_questions = database_manager.get_last_5_questions()
        return render_template("main.html", last_5_questions=last_5_questions)

@app.route("/", methods=["POST", "GET"])
def hello():
    if request.method == "POST":
        searched_word = request.form["search"]
        return redirect(url_for("search_question", search_phrase=searched_word))
    else:
        last_5_questions = database_manager.get_last_5_questions()
        return render_template("main.html", last_5_questions=last_5_questions)


@app.route("/search?q=<search_phrase>")
def search_question(search_phrase):
    search_result_q = database_manager.searched_phrase_q(search_phrase)
    search_result_a = database_manager.searched_phrase_a(search_phrase)
    return render_template("search_result.html", search_result_q=search_result_q, search_result_a=search_result_a, search_phrase=search_phrase)


@app.route('/list/', methods=["POST", "GET"])
@app.route('/list', methods=["POST", "GET"])
def list():
    if request.method == "POST":
        header = request.form["title"]
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
    all_a_data = database_manager.get_all_answer(question_id)

    comment_a_data = database_manager.get_all_comment()
    comment_q_data = database_manager.get_comment("question_id", question_id)

    all_tags = database_manager.get_tag_for_question(question_id)

    return render_template("display_question.html", comment_a_data=comment_a_data,
                           comment_q_data=comment_q_data, id=question_id, all_a_data=all_a_data,
                           current_q_data=current_q_data, all_tags=all_tags)


@app.route("/list/add-question", methods=["POST", "GET"])
def ask_question():
    time_stample = time.time()
    time_stample = datetime.fromtimestamp(time_stample)
    q_id = data_manager.create_id()
    if request.method == "POST":
        if request.form:
            database_manager.add_question(q_id, time_stample, request.form["title"], request.form["message"])

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


@app.route("/list/question/<string:question_id>/comment", methods=["POST", "GET"])
def add_q_comment(question_id):
    if request.method == "POST":
        time_stample = time.time()
        time_stample = datetime.fromtimestamp(time_stample)
        id = data_manager.create_id()
        database_manager.add_question_comment(id, question_id, request.form["comment"], time_stample)
        return redirect(url_for("display_question", question_id=question_id))
    else:
        return render_template("add_comment.html", question_id=question_id)


@app.route("/list/add-answer-image/<string:question_id>/<string:answer_id>", methods=["GET", "POST"])
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
        database_manager.add_answer(question_id, a_id, time_stample, request.form["message"])

        return redirect(url_for("display_question", question_id=question_id))

    else:
        return render_template("new_answer.html")


@app.route("/question/<question_id>/answer/<answer_id>/edit", methods=["POST", "GET"])
def edit_answer(answer_id, question_id):
    if request.method == "POST":
        database_manager.edit_answer(answer_id, request.form["message"])
        return redirect(url_for("display_question", question_id=question_id))
    else:
        current_answer_data = database_manager.get_current_answer(answer_id)
        return render_template("edit_answer.html", current_answer_data=current_answer_data)


@app.route("/question/<question_id>/answer/<answer_id>/new-comment", methods=["POST", "GET"])
def add_a_comment(answer_id, question_id):
    if request.method == "POST":
        time_stample = time.time()
        time_stample = datetime.fromtimestamp(time_stample)
        id = data_manager.create_id()
        database_manager.add_answer_comment(id, answer_id, request.form["comment"], time_stample)

        return redirect(url_for("display_question", question_id=question_id))
    else:
        return render_template("add_comment.html", question_id=question_id)


@app.route("/comment/<comment_id>/edit", methods=["POST", "GET"])
def edit_comment(comment_id):
    if request.method == "POST":
        time_stample = time.time()
        time_stample = datetime.fromtimestamp(time_stample)
        database_manager.edit_comment(request.form["comment"], time_stample, comment_id)
        answer_id = database_manager.get_current_comment(comment_id)[0]["answer_id"]

        if answer_id:
            question_id = database_manager.questionID_by_answerID(answer_id)[0]["question_id"]
        else:
            question_id = database_manager.get_current_comment(comment_id)[0]["question_id"]

        return redirect(url_for("display_question", question_id=question_id))
    else:
        current_comment = database_manager.get_current_comment(comment_id)
        return render_template("edit_comment.html", current_comment=current_comment, comment_id=comment_id)


@app.route("/question/<question_id>/edit", methods=["POST", "GET"])
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
        return render_template("edit_question.html", current_data=current_data, question_id=question_id)


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


@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    answer_id = database_manager.get_current_comment(comment_id)[0]["answer_id"]

    if answer_id:
        question_id = database_manager.questionID_by_answerID(answer_id)[0]["question_id"]
    else:
        question_id = database_manager.get_current_comment(comment_id)[0]["question_id"]

    database_manager.delete_comment(comment_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/question/<question_id>/new-tag", methods=["POST", "GET"])
def add_tag(question_id):
    id = data_manager.create_id()
    used_tags = [tag["name"] for tag in database_manager.get_tag_for_question(question_id)]

    if request.method == "POST":
        if request.form["add_new_tag"]:
            if request.form["add_new_tag"] in used_tags:
                pass
            else:
                database_manager.add_tag(id, request.form["add_new_tag"])
                database_manager.add_to_question_tag(question_id, id)

        else:
            if request.form["tags"] in used_tags:
                pass
            else:
                id = database_manager.tagID_by_tagNAME(request.form["tags"])[0]["id"]
                database_manager.add_to_question_tag(question_id, id)

        return redirect(url_for("display_question", question_id=question_id))

    else:
        all_tags = database_manager.get_all_tags()
        return render_template("tags.html", tags=all_tags)


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    database_manager.delete_question_tag(question_id, tag_id)
    return redirect(url_for("display_question", question_id=question_id))


if __name__ == "__main__":
    app.run(debug=True)

