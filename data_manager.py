import csv
import random


def create_id(id_type):
    id = 0
    while id not in id_type:
        id = str(random.randint(1, 100))
        if id not in id_type:
            id_type.append(id)
            return id



def write_csv(filename, datas):

    with open(filename, "w") as w_file:
        writer = csv.DictWriter(w_file, fieldnames=HEADERS)
        writer.writeheader()

        for i in range(len(datas)):
            writer.writerows(HEADERS)



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





ALL_QUESTION_DATAS = read_csv('sample_data/question.csv')
ALL_ANSWER_DATAS = read_csv('sample_data/answer.csv')
ALL_Q_ID = ["1","2","3"]
ALL_A_ID = ["1", "2", "3"]
HEADERS = ALL_QUESTION_DATAS[0].keys()






def main():


    print(ALL_QUESTION_DATAS)
    print("\n\n")
    print(ALL_QUESTION_DATAS[1])
    print("\n\n")
    print(ALL_QUESTION_DATAS[0]["id"])
    print("\n\n")
    for head in HEADERS:
        print(head)

    print(write_csv('sample_data/question.csv', ALL_QUESTION_DATAS))


        
if __name__ == '__main__':
    main()
