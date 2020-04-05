# main.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app.visited=0



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
	app.visited += 1
	return GiveMeSomethingResp(id=app.visited, patient=rq.dict())
	
@app.get("/hello/{name}")
async def read_item(name: str):
    return f"Hello {name}"