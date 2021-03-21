Based on the repo https://github.com/jairovadillo/pychromeless.git

This app has been created to get the petition status for a particular receipt number from the USCIS website

Update Dockerfile with your receipt number

Some beginners git commands:
git init -b main
git remote add origin  <REMOTE_URL>
git add .
git commit -m "First commit"
git remote -v
git push -u origin main

Some beginners docker commands:

make docker-build //This runs "docker-compose build"  (Check Makefile file)
make docker-run // This runs "docker-compose run lambda src.lambda_function.lambda_handler" (Check Makefile file)
docker-compose down
