from flask import Flask, render_template, request, redirect, url_for
import csv
import data_manager
import time
app = Flask(__name__)


@app.route("/")
def hello():

    return render_template("main.html")

@app.route('/list')
def list():
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
        current_q_data = [q_id, time_stample, '0', '0', request.form["title"], request.form["message"], ' ']
        data_manager.add_element('sample_data/question.csv', current_q_data)

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
        all_q_data.remove(all_q_data[index])
        time_stample = str(time.time())
        q_id = data_manager.create_id(data_manager.ALL_Q_ID)
        question = [q_id, time_stample, "0", "0", request.form["title"], request.form["message"], " "]
        data_manager.add_element("sample_data/answer.csv", question)
        return redirect(url_for("display_question", question_id=question_id))
    else:
        return render_template("edit.html", current_data=current_data)
        

@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    all_q_data = data_manager.read_csv('sample_data/question.csv')
    all_a_data = data_manager.read_csv('sample_data/answer.csv')
    for i in range(len(all_q_data)):
        if question_id == all_q_data[i][0]:
            data_manager.ALL_QUESTION_DATAS.remove(all_q_data[i])

    for i in range(len(all_a_data)):
        if question_id == all_a_data[i][0]:
            data_manager.ALL_ANSWER_DATAS.remove(all_a_data[i])

    data_manager.ALL_ID.remove(question_id)

    return redirect(url_for("list"))        
        
        

'''
@app.route("/answer/<answer_id>/delete")
def delete_(question_id):

    for i in range(len(all_a_data)):
        if question_id == all_a_data[i][0]:
            data_manager.ALL_ANSWER_DATAS.remove(all_a_data[i])

    data_manager.ALL_ID.remove(question_id)

    return redirect(url_for("list"))
'''





if __name__ == "__main__":
    app.run(debug=True)

