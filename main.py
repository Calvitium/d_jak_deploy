# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/method")
def root():
    return {"message": "GET"}

@app.put("/method")
def root():
    return {"message": "POST"}

@app.post("/method")
def root():
    return {"message": "PUT"}

@app.delete("/method")
def root():
    return {"message": "DELETE"}

@app.get("/hello/{name}")
async def read_item(name: str):
    return f"Hello {name}"