import csv
import random


def create_id():
    id = 0
    while id not in ALL_ID:
        id = str(random.randint(1, 100))
        if id not in ALL_ID:
            ALL_ID.append(id)
            return id



def read_csv(filename):
    file_list = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            file_list.append(row)
    return file_list[::-1]

ALL_QUESTION_DATAS = read_csv('sample_data/question.csv')
ALL_ANSWER_DATAS = read_csv('sample_data/answer.csv')
ALL_ID = ["1","2","3"]




"""
def main():
    print(read_csv('sample_data/question.csv'))

if __name__ == '__main__':
    main()
"""