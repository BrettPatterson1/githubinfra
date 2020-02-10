from subprocess import call
import os
import config
import create_repos
import prairielearn
import kahoot

REPO_FORMAT=config.REPO_FORMAT
GITHUB_ORGANIZATION="CS196Illinois"

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

    grades = student['grades']
    lectures = student["attendance"]
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


def add_attendance(students, lecture_attendance):
    for netid in students:
        lecture_presence = []
        for lecture in lecture_attendance:
            if netid in lecture["netids"]:
                lecture_presence.append("Lecture: {} Attended".format(lecture['name']))
            else:
                lecture_presence.append("Lecture: {} Absent".format(lecture['name']))
        students[netid]["attendance"] = lecture_presence

def main():
    students = prairielearn.grab_grades()
    attendance = kahoot.get_all_attendance()
    add_attendance(students, attendance)
    push_all_grades(students)



if __name__ == "__main__":
    main()
