from subprocess import call
import os
import config
import create_repos
import prairielearn

REPO_FORMAT=config.REPO_FORMAT
GITHUB_ORGANIZATION="CS196Illinois"

def push_all_grades(roster):
    call('git config --global credential.helper cache', shell=True)
    for student in roster:
        push_grades(student)


def push_grades(student):
    netid = student[0]
    message = 'grades'
    repo_name = REPO_FORMAT.format(netid)
    print("testing {}".format(repo_name))
    if create_repos.repo_exists(GITHUB_ORGANIZATION, repo_name):
        print("pushing grades for {}".format(repo_name))
        call('git clone https://github.com/CS196Illinois/{}.git'.format(repo_name), shell=True)
        os.chdir(repo_name)
        call('touch grades.md', shell=True)
        grade(student)
        call('git add .', shell=True)
        call('git commit -m \"grades\"', shell=True)
        call('git push origin master', shell=True)
        os.chdir('../')
        call('sudo rm -rf ' + repo_name, shell=True)


# place the grades for a netid into a markdown file
def grade(student):
    netid = student[0]
    grades = student[1]
    with open('grades.md', 'w+') as f:
        f.write('# CS 196 Grades for ' + netid)
        f.write('\n')
        f.write('## Homework')
        f.write('\n')
        for assignment in grades:
            (label, name, points, max_points, percentage) = assignment
            f.write('{} ({}) Score: {}/{} Percentage: {}%'.format(label, name, points, max_points, percentage))
            f.write('\n')


def main():
    student_info = prairielearn.grab_grades()
    push_all_grades(student_info)



if __name__ == "__main__":
    main()
