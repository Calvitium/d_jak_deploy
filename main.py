# main.py
######################################################################
######################################################################
#####################       ASSIGNMENT 1       #######################
######################################################################
######################################################################

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
app.ID = 0
app.patients = {}


### TASK 1 ###########################################################

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

### TASK 2 ###########################################################

@app.get("/method")
def root():
    return {"method": "GET"}

@app.put("/method")
def root():
    return {"method": "PUT"}

@app.post("/method")
def root():
    return {"method": "POST"}

@app.delete("/method")
def root():
    return {"method": "DELETE"}

### TASK 3 ###########################################################

class GiveMeSomethingRq(BaseModel):
	name: str
	surename: str

class GiveMeSomethingResp(BaseModel):
	id: int
	patient: dict

@app.post("/patient", response_model=GiveMeSomethingResp)
def receive_patient(rq: GiveMeSomethingRq):
	if app.ID not in app.patients.keys():
		app.patients[app.ID] = rq.dict()
		app.ID += 1
	return GiveMeSomethingResp(id=app.ID, patient=rq.dict())

### TASK 4 ###########################################################
	
@app.get("/patient/{pk}")
async def return_patient(pk: int):
    if pk in app.patients.keys():
    	return app.patients[pk]
    else:
    	raise HTTPException(status_code=204, detail="Item not found")

######################################################################
######################################################################
#####################       ASSIGNMENT 3       #######################
######################################################################
######################################################################


### TASK 1 ###########################################################

@app.get("/welcome")
def do_welcome():
	return {"message": "Sram Ci na klatę"}


### TASK 2 ###########################################################
from hashlib import sha256
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, Response
import secrets

security = HTTPBasic()
app.secret_key = "very constatn and random secret, best 64 characters, here it is."

session_tokens = []

@app.post("/login")
def get_current_user(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    session_tokens.append(session_token)
    response.headers["Location"] = "/welcome"

### TASK 3 ###########################################################
from fastapi import Cookie

@app.post("/logout")
def logout(*, response: Response, session_token: str = Cookie(None)):
	if session_token not in session_tokens:
		raise HTTPException(status_code=401, detail="Unathorised")
	session_tokens.delete(session_token)
	return RedirectResponse("/")

### TASK 4 ###########################################################


from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from typing import List
from hashlib import sha256

templates = Jinja2Templates(directory="templates")


@app.get("/items/{id}")
def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "my_string": "Wheeeee!", "my_list": [0,1,2,3,4,5]})


@app.get("/hello/")
def hello():
    return {"hello_world": "hello_world"}


@app.get("/simple_path_tmpl/{sample_variable}")
def simple_path_tmpl(sample_variable: str):
    print(f"{sample_variable=}")
    print(type(sample_variable))
    return {"sample_variable": sample_variable}


objects = {
    1: {"field_a": "a", "field_b": "b"},
    2: {"field_a": "a", "field_b": "b"},
    3: {"field_a": "a", "field_b": "b"},
    # .... #
}



@app.get("/v2/simple_path_tmpl/{obj_id}/{field}")
def simple_path_tmpl(obj_id: int, field: str):
    print(f"{obj_id=}")
    print(f"{field=}")
    return {"field": objects.get(obj_id, {}).get(field)}


@app.get("/v2/items/")
def read_items(*, ads_id: str = Cookie(None)):
    return {"ads_id": ads_id}


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}


