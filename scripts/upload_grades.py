from subprocess import call
import os
import config
import create_repos
import prairielearn
import kahoot
import csv

PROJECT_PATH=config.PROJECT_PATH_LINUX
REPO_FORMAT=config.REPO_FORMAT
GITHUB_ORGANIZATION="CS196Illinois"
WinnerLectures = ("Rust 1", "Rust 2", "Rust 3", "Google Scavenger Hunt", "Regular Expressions","Concurrency 2", "Dynamic Programming", "Recursive Backtracking", "Stacks", "Concurrency 1", "Functional Programming")
MemeContestWinners = ("jessep2", "aehasan2", "jplacko2", "pnl2", "lz15", "apillai5")
hw_to_lecture = {"ATT0": "Regular Expressions", "ATT1": "Data mining", "ATT2": "Smart Pointers Linked Lists", "ATT3": "Stacks", "ATT4": "Fearless Recursion",
                 "ATT5": "Dynamic Programming", "ATT6": "Functional Programming", "ATT7": "Recursive Backtracking", "ATT8": "Concurrency 1", "ATT9": "Concurrency 2"}
form_eval = set()


def push_all_grades(students):
    call('git config --global credential.helper cache', shell=True)
    for netid, profile in students.items():
        push_grades(netid, profile)


def push_grades(netid, student):
    repo_name = REPO_FORMAT.format(netid)
    print("testing {}".format(repo_name))
    if create_repos.repo_exists(GITHUB_ORGANIZATION, repo_name):
        print("pushing grades for {}".format(repo_name))
        call('git clone https://github.com/CS196Illinois/{}.git'.format(repo_name), shell=True)
        os.chdir(repo_name)
        call('touch grades.md', shell=True)
        grade(netid, student)
        call('git add .', shell=True)
        call('git commit -m \"grades\"', shell=True)
        call('git push origin master', shell=True)
        os.chdir('../')
        call('sudo rm -rf ' + repo_name, shell=True)
    else:
        print("{} not found".format(repo_name))

# place the grades for a netid into a markdown file
def grade(netid, student):
    #for 1+ bash hw
    if netid == "sv23":
        student["extra_credit"] += 1
    grades = student['grades']
    lectures = []
    if 'attendance' in student:
        lectures= student["attendance"]
    with open('grades.md', 'w+') as f:
        f.write('# CS 196 Grades for ' + netid)
        f.write('\n')
        f.write('## Homework')
        f.write('\n')
        for assignment in grades:
            (label, name, points, max_points, percentage) = assignment
            f.write('{} ({}) Score: {}/{} Percentage: {}%'.format(label, name, points, max_points, percentage))
            f.write('\n\n')
        f.write('\n')
        f.write('## Lecture Attendance')
        f.write('\n')
        for lecture in lectures:
            f.write(lecture)
            f.write('\n\n')
        f.write('\n')
        f.write("## Project Grades")
        f.write('\n')
        f.write("Midterm: Score: 5/5 Percentage: 100%")
        f.write('\n\n\n')
        f.write("## Misc EC")
        f.write('\n')
        if (netid in MemeContestWinners):
            f.write("Meme Contest Winner! +1 EC")
            student["extra_credit"] += 1
            f.write('\n\n')
        if (netid in form_eval):
            f.write("Filled out course evaluation form +3 EC")
            student["extra_credit"] += 3
            f.write('\n\n')
        f.write('\n\n\n')
        if "final" in student:
            f.write("## FINAL GRADES")
            f.write('\n\n')
            f.write("Information: Each homework is weighted the same, you get 6 lecture drops, and extra credit is max 10 points ")
            f.write('\n\n')
            f.write("Grading distribution is as follows: 10% lecture, 65% project, 25% Homework, 10% Extra credit")
            f.write('\n\n')
            f.write("Homework: {}%".format(student['final']['homework']))
            f.write('\n\n')
            f.write("Lecture: {}%".format(student['final']['attendance']))
            f.write('\n\n')
            f.write("Project: {}%".format(student['final']['project']))
            f.write('\n\n')
            ec = min(student['extra_credit']/10, 1) * 100
            f.write("Extra Credit: {}%".format(ec))
            f.write('\n\n')
            final_score = min(100, ec) * .1 + min(100, student['final']['homework']) * .25 + min(100, student['final']['attendance']) * .1 + min(100, student['final']['project'])* .65
            letter_grade = ""
            if final_score >= 97:
                letter_grade = "A+"
            elif final_score >= 93:
                letter_grade = "A"
            elif final_score >= 90:
                letter_grade = "A-"
            elif final_score >= 87:
                letter_grade = "B+"
            elif final_score >= 83:
                letter_grade = "B"
            elif final_score >= 80:
                letter_grade = "B-"
            elif final_score >= 77:
                letter_grade = "C+"
            elif final_score >= 73:
                letter_grade = "C"
            elif final_score >= 70:
                letter_grade = "C-"
            elif final_score >= 60:
                letter_grade = "D"
            else:
                letter_grade = "F"
            f.write("Final Grade: {}% {}".format(final_score, letter_grade))



def add_attendance(students, lecture_attendance):
    for netid in students:
        lecture_presence = []
        if 'final' in students[netid]:
            students[netid]["final"]["attendance"] = 0
            for name in lecture_attendance:
                lecture = lecture_attendance[name]
                note = ""
                if netid in lecture["netids"]:
                    note += "Lecture: {} Attended ".format(lecture['name'])
                    students[netid]["final"]["attendance"] += 1
                else:
                    note += "Lecture: {} Absent ".format(lecture['name'])
                if lecture['name'] in WinnerLectures and netid in lecture["winners"]:
                    note += "   Winner! +1% Extra Credit"
                    students[netid]["extra_credit"] += 1
                lecture_presence.append(note)
            students[netid]["attendance"] = lecture_presence
            students[netid]["final"]["attendance"] = min(1, students[netid]["final"]["attendance"] / 16) * 100

def combine_kahoot_and_prairielearn(students, attendance):
    for netid in students:
        for i in range(10):
            label, name, points, max_points, percentage = students[netid]['grades'][i]
            if percentage is not None and percentage == 100:
                lecture_name = hw_to_lecture[label]
                attendance[lecture_name]["netids"].add(netid)
        # get rid of attendance assignments
        students[netid]['grades'] = students[netid]['grades'][10:]
    #print(students["nikilr2"]["final"])
    return students, attendance

def grab_final_grades(students):
    filename = PROJECT_PATH + "/data/indiv.csv"
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            netid = line[0]
            students[netid]["final"] = {}
            #print(students[netid])
            students[netid]["final"]["project"] = float(line[1])
            if students[netid]["final"]["project"] > 100:
                students[netid]["extra_credit"] += (students[netid]["final"]["project"] - 100)
    return students

def calc_homework_score(students):
    for netid in students:
        if "final" in students[netid]:
            hw_percentage = 0
            for assignment in students[netid]['grades']:
                # assignment 4 is percentage
                if assignment[4] is None:
                    continue
                elif assignment[4] == 110:
                    hw_percentage += 100
                else:
                    hw_percentage += assignment[4]
            students[netid]["final"]["homework"] = min(hw_percentage / 7, 100)

def get_form_eval():
    filename = PROJECT_PATH + "/data/eval.csv"
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            netid = line[1]
            form_eval.add(netid)


def main():
    get_form_eval()
    students = prairielearn.grab_grades()
    attendance = kahoot.get_all_attendance()
    students = grab_final_grades(students)
    #print(students["nikilr2"]["final"])
    students, attendance = combine_kahoot_and_prairielearn(students, attendance)
    #print(students["nikilr2"]["final"])
    add_attendance(students, attendance)
    calc_homework_score(students)
    push_all_grades(students)



if __name__ == "__main__":
    main()
