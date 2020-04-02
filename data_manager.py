import csv
import random
import operator


def create_id(id_type):
    id = 0
    while id not in id_type:
        id = str(random.randint(1, 100))
        if id not in id_type:
            id_type.append(id)
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
    print(HEADERS)
    print(ALL_QUESTION_DATAS)


        
if __name__ == '__main__':
    main()
