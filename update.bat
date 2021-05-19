git add .
git status
set /p msg="Enter Commit Message: "
git commit -m "%msg%"
git push -u origin main