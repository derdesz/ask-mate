import csv


def read_csv(filename):
    file_list = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            file_list.append(row)
    file_list = file_list.reverse()
    return file_list




#def main():
#    read_csv('sample_data/question.csv')

#if __name__ == '__main__':
#    main()