# fastapi-postgresql-crud

# Setup

## Create vitrual environment

_Terminal_
`python3 -m venv .venv`

## Activate it

_Terminal_
`. .venv/bin/activate`

## Add `.gitignore`

- inlcude `.venv`

## Install `pip`

_Terminal_
`pip install --upgrade pip`

## Install `fastapi`

- You can install specific by putting it inside the []
  _Terminal_
  `pip install 'fastapi[standard]'`

## Add `requirements.txt`

_Terminal_
`pip freeze > requirements.txt`

## Install Package (Requirements)

- Add the package in `requirements.txt`
  _Terminal_
  `pip install -r requirements.txt`
- Or install the package first, then update the `requirements.txt`
  _Terminal_
  `pip install package_name`
  _Terminal_
  `pip freeze > requirements.txt`

## If no repository

_Terminal_
`git init`

_Terminal_
`git add .`

_Terminal_
`git commit -m "initial commit"`

## Create `main.py`

_Terminal_
`touch main.py`

## Update the `main.py`

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

```

# You can immediately access `swagger` & `openapi`

- Swagger: `localhost:800/docs`
- OpenApi: `localhost:800/openapi.json`
