import urllib.request
import json
import requests
import config

PRAIRIELEARN_TOKEN = config.PRAIRIELEARN_TOKEN


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
        if (gradebook[i]['user_role'] == 'Instructor' or gradebook[i]['user_role'] == "TA"):
            continue
        just_students.append(gradebook[i])
    return just_students


def get_netid(email):
    return email.split("@")[0].strip().lower()

def get_assignments(student):
    assessments = student['assessments']
    all_grades = []
    for hw in assessments:
        label = hw['assessment_label']
        name = hw['assessment_name']
        points = hw['points']
        max_points = hw['max_points']
        percentage = hw['score_perc']
        assignment = (label, name, points, max_points, percentage)
        all_grades.append(assignment)
    sorted_grades = sorted(all_grades, key=lambda x: x[0])
    return sorted_grades
        
def extract_relevant_data(students):
    profiles = {}
    for student in students:
        netid = get_netid(student['user_uid'])
        grades = get_assignments(student)
        profile = {
            "grades": grades
        }
        profiles[netid] = profile
    return profiles

#Returns nested list [netid, grades]
def grab_grades():
    gradebook = get_grades_from_prairielearn()
    students = filter_out_instructors(gradebook)
    student_info = extract_relevant_data(students)
    return student_info

def main():
    gradebook = get_grades_from_prairielearn()
    students = filter_out_instructors(gradebook)
    student_info = extract_relevant_data(students)
    print(student_info)

if __name__ == "__main__":
    main()