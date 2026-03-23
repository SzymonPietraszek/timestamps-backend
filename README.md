This repo is used to deploy fastAPI on AWS lambda. It is refered in terraform-templates repo. All the code must be placed in app folder.

# Local development
Go to AWS and create a dynamodb with TABLE_NAME=db TABLE_PK=pk. Run `aws configure` to allow a connection.

```
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
ACTIONS="a,b,c" TIME_VALUES="0,1,2,3" TABLE_NAME=test TABLE_PK=pk uvicorn app.main:app --reload --port 8000
deactivate
```
