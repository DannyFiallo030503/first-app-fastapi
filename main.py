from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

addin = [2,3,4]

# tipos de esquemas 
class FirstModel(BaseModel):
    n: int
    m: int

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
@app.get('/query/{query}', tags=['Home'])
def get_query(query: str, number: int):
    return query



# con los metodos post que se le pasan parametros como query se puede agregar valores
@app.post('/post/{n}', tags=["Post"])
def posting(n: int , m: int = Body()):
    addin.append(n + m)
    return addin



# con el metodo put logramos actualizar valores dado un valor (Update)
@app.put('/put/{n}', tags=['Put'])
def puts(n: int , m: int = Body()):
    for i in range(0, len(addin) - 1):
        if addin[i] == n:
            addin[i] += m
    return addin



# sin mas ni menos es un delete elimina un valor dado
@app.delete('/delete/{n}', tags=['Delete'])
def deleting(n: int):
    for i in addin:
        if i == n:
            addin.remove(i)
    return addin



# utilizaciond de esquemas 
@app.post("/Squema/post/{n}", tags=["Squema"])
def post_squema(n: int, sqm: FirstModel):
    addin.append(sqm.m + sqm.n)
    return addin

@app.put('/Squema/put/{n}', tags=['Squema'])
def puts_squema(n: int, sqm: FirstModel):
    for i in range(0, len(addin) - 1):
        if addin[i] == sqm.n:
            addin[i] += sqm.m
    return addin

@app.delete("/Squema/delete/{n}", tags=['Squema'])
def deleting_squema(n: int, sqm: FirstModel):
    for i in addin:
        if i == sqm.n + sqm.m:
            addin.remove(i)
    return addin