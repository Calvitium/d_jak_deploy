# main.py

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