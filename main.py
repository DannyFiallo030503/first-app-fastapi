from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# modificando la ruta de docs
app.title = "Mi app"
app.version = "v0.1"

# devuelve un string si no existe una ruta
@app.get('/', tags=['Home'])
def home():
    return "Hola" 

# al usar esa ruta genera un response que es html
@app.get('/home', tags=['Home'])
def home():
    return HTMLResponse('<h1> hola </h1>')

# se le introduce el valor a la ruta y la mustra
@app.get('/{id}', tags=["Home"])
def get_id(id: int):
    return id

# se le introduce en forma de query despues de la / de esta manera /?<variable>=<valor>
# si es mas de un valor entonces /?<variable>=<valor>&<variable>=<valor>
@app.get('/query/', tags=['Home'])
def get_query(query: str, number: int):
    return query