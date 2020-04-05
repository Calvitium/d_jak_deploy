# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/GET")
def root():
    return {"message": "GET"}

@app.get("/POST")
def root():
    return {"message": "POST"}

@app.get("/PUT")
def root():
    return {"message": "PUT"}

@app.get("/DELETE")
def root():
    return {"message": "DELETE"}

@app.get("/hello/{name}")
async def read_item(name: str):
    return f"Hello {name}"