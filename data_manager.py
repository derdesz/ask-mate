import csv
import random
import operator
import database_manager


def create_id():

    id = random.randint(1, 10000)
    return id




def write_csv(datas, file_name, headers):
    with open(file_name, "w") as file:
        csv_writer = csv.DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        csv_writer.writerows(datas)


def read_csv(filename):
    all_data = []
    with open (filename, "r") as file:
        csv_reader = csv.DictReader(file)
        for rows in csv_reader:
            all_data.append(rows)
        return all_data


def add_element(filename, datas):
    with open(filename, "a") as file:
        row = ",".join(datas)
        file.write(row + "\n")


def read_sorted_csv(filename, header, reverse):
    all_data = []
    with open (filename, "r") as file:
        csv_reader = csv.DictReader(file)
        data = sorted(csv_reader, key=operator.itemgetter(header), reverse=reverse)

        if header == "title" or header == "message" or header == "submission_time":
            pass
        else:
            for row in data:
                row[header] = int(row[header])
            data = sorted(data, key=operator.itemgetter(header), reverse=reverse)

        for rows in data:
            all_data.append(rows)
        return all_data

def create_id_list(data):
    l = []
    for row in data:
        l.append(row["id"])
    return l


QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
ALL_QUESTION_DATAS = read_csv('sample_data/question.csv')
ALL_ANSWER_DATAS = read_csv('sample_data/answer.csv')
ALL_Q_ID = create_id_list(read_csv('sample_data/question.csv'))
ALL_A_ID = create_id_list(read_csv('sample_data/answer.csv'))