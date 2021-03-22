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

Can connect and write to Dynamodb
- Create user in IAM with access to read and write from Dynamo db. Generate programatic access keys for user.
- Set  the following in the docker-compose.yml file
        - AWS_ACCESS_KEY_ID=<From iam user with access to dynamodb>
        - AWS_SECRET_ACCESS_KEY=<From iam user with access to dynamodb>
        - AWS_REGION=<Region of Dyanmodb>
- Create dynamo db table named "receipt_status" with primary key "receipt_number" and sort key "update_date". Both data types String.

03/21/2021
- Added functionality to write to Lambda
