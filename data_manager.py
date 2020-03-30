import csv




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





"""
def main():
    print(read_csv('sample_data/question.csv'))

if __name__ == '__main__':
    main()
"""