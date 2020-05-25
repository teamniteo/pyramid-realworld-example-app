set -xeu

# Fetch unshallow
git fetch --unshallow

# Update the python packages
poetry update

# Only continue if there are any changes
if ! git diff-index --quiet HEAD; then
  today=$(date -I)
  # Commit the new changes and push them to the repository so a PR can be opened
  git checkout -b "poetry-update-$today"
  git config user.name "poetry updater"
  git add poetry.lock
  git commit -m "poetry update $today"
  git push -u origin "poetry-update-$today"
  curl -X POST -L https://api.github.com/repos/${GITHUB_REPOSITORY:?}/pulls \
	-H "Accept: application/vnd.github.v3+json" \
	-H "Authorization: Bearer ${GITHUB_TOKEN:?}" \
  	-d '{"title": "Update Python Packages", "head": "poetry-update-'$today'", "base": "master"}' \
	--fail
fi
