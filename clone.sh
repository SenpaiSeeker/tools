REPO_CLONE=$1
REPO_REMOTE=$2
GITHUB_TOKEN=$3
COMMIT_MESSAGE=${4:-"initial"}

git clone "$REPO_CLONE"
cd "$(basename "$REPO_CLONE" .git)"

rm -rf .git
git config --global user.email "support@hacker.ltd"
git config --global user.name "hacker"
git init

git add .
git commit -m "$COMMIT_MESSAGE"
git branch -M main

REPO_REMOTE_CLEAN="${REPO_REMOTE#https://}"

git remote add origin "$REPO_REMOTE"
git remote set-url origin "https://$GITHUB_TOKEN@$REPO_REMOTE_CLEAN"

git push -u origin main
