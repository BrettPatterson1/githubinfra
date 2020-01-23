source ~/.bash_profile

name=$(curl --header "Authorization: token $GITHUB_TOKEN" \
	https://api.github.com/repos/BrettPatterson1/Genome_Parser/collaborators/BrettPatterson1/permission)

echo "$name"
