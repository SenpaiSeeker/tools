git config --global user.email "support@norsodikin.ltd"
git config --global user.name "ɴᴏʀ sᴏᴅɪᴋɪɴ"

BRANCH=$(git rev-parse --abbrev-ref HEAD)

git checkout --orphan temp-branch
git add -A
COMMIT_MESSAGE=$(TZ=Asia/Jakarta date +"%Y-%m-%d %H:%M:%S")
git commit -m "$COMMIT_MESSAGE"

git branch -D "$BRANCH"
git branch -m "$BRANCH"
git push --force origin "$BRANCH"
