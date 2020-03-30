# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/hello/{name}")
async def read_item(name: str):
    return f"Hello {name}"