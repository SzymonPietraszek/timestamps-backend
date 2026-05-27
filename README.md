This repo is used to deploy fastAPI on AWS lambda. It is refered in terraform-templates repo. All the code must be placed in app folder.


# Prerequisites:
You should first deploy the infrastructure (terraform repo) and use its output to finish these steps:
1. Enable github actions. Actions -> I understand my workflows, go ahead and enable them
2. Add two github secrets with correct values from infrastructure deployment (terraform output). Settings -> Secrets and variables -> Actions -> New repository secret ->
```
Name: AWS_ACCOUNT_ID
Secret: <123456789>
```
```
Name: AWS_ROLE_FOR_GITHUB_ACTIONS
Secret: <fwf-github-actions>
```
3. Update build.env file with correct values.


# Local development
Go to AWS and create a dynamodb with TABLE_NAME=db TABLE_PK=pk. Run `aws configure` to allow a connection.

```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt
ACTIONS="a,b,c" TIME_VALUES="0,1,2,3" TABLE_NAME=test TABLE_PK=pk uvicorn app.main:app --reload --port 8000
deactivate
```
