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
app.patients = {"trudnY": "PaC13Nt"}
app.session_tokens = []
app.secret_key = "very constatn and random secret, best 64 characters, here it is."

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
from fastapi import Depends, Response, status
import secrets

security = HTTPBasic()


@app.post("/login")
def get_current_user(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    app.session_tokens.append(session_token)
    response.headers["Location"] = "/welcome"
    response.status_code = status.HTTP_302_FOUND 

### TASK 3 ###########################################################
from fastapi import Cookie

@app.post("/logout")
def logout(*, response: Response, session_token: str = Cookie(None)):
	if session_token not in app.session_tokens:
		raise HTTPException(status_code=401, detail="Unathorised")
	app.session_tokens.remove(session_token)
	return RedirectResponse("/")

### TASK 4 ###########################################################

