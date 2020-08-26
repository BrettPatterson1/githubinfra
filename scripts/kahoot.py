#import openpyxl
import os
import config
import csv

PROJECT_PATH=config.PROJECT_PATH_WINDOWS
PROJECT_PATH=config.PROJECT_PATH_LINUX
## initializing the xlsx
#wb = openpyxl.load_workbook(r'C:\Users\brett\OneDrive\Desktop\githubinfra\data\Bash 2.xlsx')


## getting all sheet names
def create_attendance(filename):
    attendance = {}
    wb = openpyxl.load_workbook(filename)
    scores = wb['Final Scores']
    #Cell A1 of Final Scores sheet is the name of the quiz
    attendance["lecture_name"] = str(scores["A1"].value)
    attendance["netids"] = set()
    data = scores.rows
    #student entrys start in the 4th row (row 3)
    #student kahoot name is 2th column (1)
    for i in range(3, len(data)):
        attendance['netids'].add(normalize_name(str(data[i][1].value)))


def normalize_name(name):
    return name.strip().lower()

def get_data_dir():
    return PROJECT_PATH + "/data/kahoot"

def create_csv(filename):
    wb = openpyxl.load_workbook(filename)
    scores = wb['Final Scores']

    ## getting the data from the sheet
    data = scores.rows
    ## creating a csv file
    csv = open(filename[:-4] + "csv", "w+")

    for row in data:
        l = list(row)
        info = []
        for i in range(len(l)):
            info.append(str(l[i].value))
        csv.write(",".join(info))
        csv.write('\n')

def create_all_csvs(filenames):
    for filename in filenames:
        create_csv(filename)

def get_filenames(extension):
    data_dir = get_data_dir()
    names = []
    for file in os.listdir(data_dir):
        if file.endswith(extension):
            names.append(os.path.join(data_dir, file))
    print(names)
    return names

def read_csv(filename):
    attendance = {}
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)
        all_students = set() #to skip duplicate forms
        winners = set()
        i = 0
        for line in csv_reader:
            if i == 0:
                attendance["name"] = line[0]
                i+=1
                continue
            elif i < 3:
                i+=1
                continue
            netid = line[1].strip().lower()
            if i < 8:
                winners.add(netid)
            i+=1
            all_students.add(netid)
    attendance["netids"] = all_students
    attendance["winners"] = winners
    return attendance

def get_all_attendance():
    files = get_filenames(".csv")
    all_attendance = {}
    for file in files:
        lecture_info = read_csv(file)
        all_attendance[lecture_info['name']] = lecture_info
    return all_attendance

def main():
    create_all_csvs(get_filenames(".xlsx"))

if __name__ == "__main__":
    main()