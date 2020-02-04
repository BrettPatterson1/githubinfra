import urllib.request
import json
import requests

PRAIRIELEARN_TOKEN = "592a6c33-4747-457e-97d1-8024bed832e3"


def get_grades_from_prairielearn():
    header={
        "Private-Token": PRAIRIELEARN_TOKEN
    }
    url = "https://prairielearn.engr.illinois.edu/pl/api/v1/course_instances/53634/gradebook"

    r = requests.get(url, headers=header)
    return r.json()


def filter_out_instructors(gradebook):
    just_students = []
    for i in range(len(gradebook)):
        if gradebook[i]['user_role'] == 'Instructor':
            continue
        just_students.append(gradebook[i])
    return just_students


def get_netid(email):
    return email.split("@")[0]

def get_assignments(student):
    assessments = student['assessments']
    all_grades = []
    for hw in assessments:
        label = hw['assessment_label']
        name = hw['assessment_name']
        
def extract_relevant_data(students):
    for student in students:
        netid = get_netid('user_uid')


def main():
    gradebook = get_grades_from_prairielearn()
    students = filter_out_instructors(gradebook)
    student_info = extract_relevant_data(students)

if __name__ == "__main__":
    main()