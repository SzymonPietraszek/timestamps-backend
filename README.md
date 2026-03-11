This repo is used to deploy fastAPI on AWS lambda. It is refered in terraform-templates repo. All the code must be placed in app folder.

# Local development
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload
http://127.0.0.1:8000/docs
```
