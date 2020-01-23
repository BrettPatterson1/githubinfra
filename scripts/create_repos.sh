# $1 is the netid of the student

# Allows us to use our bashrc and bash_profile
source ~/.bash_profile

repo_name="sp20-$1"

# Create the project
create_project_response=$(curl --header "Authorization: token $GITHUB_TOKEN" \
    --request POST \
    --form "name=$repo_name" \
    --form "private=true"\
    https://api.github.com/orgs/CS196Illinois/repos)

# Get their gitlab username using their netid
github_username=$(bash scripts/get_user_id.sh $1)

echo "$github_username"

# github access levels
admin="admin"
write="write"
reading="read"
none="none"

# Add them to the project group as a maintainer
curl --header "Authorization: token $GITHUB_TOKEN" \
    --request PUT \
    --form "permission=$reading" \
    https://api.github.com/repos/BrettPatterson1/$repo_name/collaborators/$github_username


