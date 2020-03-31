from flask import Flask, render_template, request, redirect, url_for
import csv
import data_manager
app = Flask(__name__)


@app.route("/")
def hello():

    return render_template("main.html")

@app.route('/list')
def list():
    return render_template('list.html', rows=len(data_manager.ALL_QUESTION_DATAS), all_data=data_manager.ALL_QUESTION_DATAS)

@app.route("/list/question/<string:question_id>")
def display_question(question_id):
    all_q_data = data_manager.ALL_QUESTION_DATAS
    all_a_data = data_manager.ALL_ANSWER_DATAS
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i][0]:
            current_q_data = all_q_data[i]

    for i in range(len(all_a_data)):
        if question_id == all_a_data[i][0]:
            current_a_data = all_a_data[i]



    return render_template("display_question.html", id=question_id, current_a_data=current_a_data, current_q_data=current_q_data,
                           q_rows=len(data_manager.ALL_QUESTION_DATAS),
                           a_rows=len(data_manager.ALL_ANSWER_DATAS), a_col=(len(current_a_data) - 1))


@app.route("/list/add-question", methods=["POST", "GET"])
def ask_question():
    q_id = data_manager.create_id()

    if request.method == "POST":
        datas = [request.form["title"], request.form["message"]]
        data_manager.ALL_QUESTION_DATAS.append([q_id, "", "", "", datas[0], datas[1], ""])
        data_manager.ALL_ANSWER_DATAS.append([q_id, "", "", "", "", "51340"])
        return redirect(url_for("display_question", question_id=q_id))
    else:
        return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def new_answer(question_id):
    if request.method == "POST":
        all_asw = data_manager.ALL_ANSWER_DATAS
        for i in range(len(all_asw)):
            if question_id == all_asw[i][0]:
                data_manager.ALL_ANSWER_DATAS[i].insert(4, request.form["message"])
        return redirect(url_for("display_question", question_id=question_id))
    else:
        return render_template("new_answer.html")


@app.route("/question/<question_id>/edit", methods=["POST","GET"])
def edit_question(question_id):
    all_q_data = data_manager.ALL_QUESTION_DATAS
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i][0]:
            current_data = all_q_data[i]

    if request.method == "POST":
        current_data[4] = request.form["title"]
        current_data[5] = request.form["message"]
        return redirect(url_for("display_question", question_id=question_id))
    else:
        return render_template("edit.html", current_data=current_data)

'''
@app.route("/answer/<answer_id>/delete")
def delete_(question_id):

    for i in range(len(all_a_data)):
        if question_id == all_a_data[i][0]:
            data_manager.ALL_ANSWER_DATAS.remove(all_a_data[i])

    data_manager.ALL_ID.remove(question_id)

    return redirect(url_for("list"))
'''



@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    all_q_data = data_manager.ALL_QUESTION_DATAS
    all_a_data = data_manager.ALL_ANSWER_DATAS
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i][0]:
            data_manager.ALL_QUESTION_DATAS.remove(all_q_data[i])

    for i in range(len(all_a_data)):
        if question_id == all_a_data[i][0]:
            data_manager.ALL_ANSWER_DATAS.remove(all_a_data[i])

    data_manager.ALL_ID.remove(question_id)

    return redirect(url_for("list"))

if __name__ == "__main__":
    app.run(debug=True)

id,submission_time,vote_number,question_id,message,image
