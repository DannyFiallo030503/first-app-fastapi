from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

app.title = "Mi app"
app.version = "v0.1"

@app.get('/', tags=['Home'])
def home():
    return "Hola" 

@app.get('/home', tags=['Home'])
def home():
    return HTMLResponse('<h1> hola </h1>')

@app.get('/{id}', tags=["Home"])
def get_id(id: int):
    return id