import requests
import csv
import json
import config

data=r"C:\Users\brett\OneDrive\Desktop\githubinfra\data\netid_github_sp20.csv"
REPO_FORMAT=config.REPO_FORMAT
GITHUB_TOKEN=config.GITHUB_TOKEN
GITHUB_ORGANIZATION="CS196Illinois"
GITHUB_USERNAME="BrettPatterson1"
HEADERS = {"Authorization": "token {}".format(config.GITHUB_TOKEN)}

def read_csv(filename):
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)

        next(csv_reader) # skip heading
        all_students = set() #to skip duplicate forms
        #Might have to change based on your data
        for line in csv_reader:
            netid = line[2].strip()
            github = line[3].strip()
            all_students.add((netid, github))

        return all_students

# Realized organization is owner
def repo_exists(owner, repo_name):
    r = requests.get("https://api.github.com/repos/{}/{}".format(owner, repo_name), headers=HEADERS)
    #200 means OK
    if r.status_code == 200:
        return True
    return False

def create_repo(repo_name, netid):
    payload = {
        "name": repo_name,
        "private": "true",
        "visibility": "private",
        "description": "A repository for {}'s CS 196 Sp 20 grades".format(netid)
    }
    r = requests.post("https://api.github.com/orgs/{}/repos".format(GITHUB_ORGANIZATION), headers=HEADERS, data=json.dumps(payload))
    if r.status_code == 201:
        print("created {}".format(repo_name))
    else:
        print("Error in creating {} because {}".format(repo_name, r.json()['errors'][0]['message']))
    return repo_name

def add_collaborator(owner, repo_name, github_username):
    #permission can be pull, push, or admin
    payload = {
        "permission": "pull",
    }
    r = requests.put("https://api.github.com/repos/{}/{}/collaborators/{}".format(owner, repo_name, github_username), headers=HEADERS, data=json.dumps(payload))
    if r.status_code == 204:
        print("{} is already a collaborator for {}".format(github_username, repo_name))
    elif r.status_code == 201:
        print("Invitation created for {} to join {}".format(github_username, repo_name))
    else:
        print("ERROR UPON INVITATION for {} to join {}".format(github_username, repo_name))
        print(r.json())

#for testing
def show_repos():
    r = requests.get("https://api.github.com/user/repos", headers=HEADERS)
    for repo in r.json():
        print(repo['name'])

def get_existing_org_repos():
    payload = {
        "type": "all"
    }
    r = requests.get("https://api.github.com/orgs/{}/repos".format(GITHUB_ORGANIZATION), headers=HEADERS, data=json.dumps(payload))
    for repo in r.json():
        print(repo['name'])

def get_user_repos():
    r = requests.get("https://api.github.com/users/{}/repos".format(GITHUB_USERNAME), headers=HEADERS)
    for repo in r.json():
        print(repo['name'])

#Does occasionally run into errors if wrong github is entered
def make_all_repos(students):
    for student in students:
        netid = student[0]
        github = student[1]
        repo_name = REPO_FORMAT.format(netid)
        if repo_exists(GITHUB_ORGANIZATION, REPO_FORMAT.format(netid)):
            continue
        else:
            create_repo(repo_name=repo_name, netid=netid)
            add_collaborator(GITHUB_ORGANIZATION, repo_name=repo_name, github_username=github)


def main():
    students = read_csv(data)
    make_all_repos(students)

if __name__ == '__main__':
    main()

