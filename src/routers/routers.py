from fastapi import FastAPI, HTTPException,Body, Query, Path
from fastapi.responses import HTMLResponse, Response
from src.models.models import FirstModel, ValModel, FirstModelValidate, Thing
from fastapi import APIRouter, Query, Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

# DB
DATABASE_URL = "postgresql://myuser:123@localhost:5432/prueba-fastapi"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# app de rutas que se le puede agregar a la principal, tiene varios atributos que son utiles como prefix
app = APIRouter(prefix='/Routes')

addin = []
 

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




# utilizando esquemas validados
@app.post('/Squema/validate/post', tags=['Squema Validate'])
def post_squema_validate(sqmv: FirstModelValidate):
    addin.append(sqmv.m + sqmv.n)
    return addin

@app.get('/Squema/validate/get/', tags=['Squema Validate'])
def get_squema_validate_query(n: int = Query(gt=0)):
    x = None
    for i in addin:
        if i == n:
            x = i
    response = Response(x)
    if x == None:
        response =  Response(x, status_code=404)
    return response

@app.get('/Squema/validate/get/{n}', tags=['Squema Validate'])
def get_squema_validate_path(n: int = Path(lt=0)):
    x = None
    for i in addin:
        if i == n:
            x = i
    return x

@app.post('/Squema/validator/validator/post', tags=['Squema Validate'])
def get_ssquema_validate_val(sqm: ValModel):
    addin.append(sqm.j)
    return addin


@app.post("/add/{value}", tags=['BD'])
def add_value(value: str):
    session = SessionLocal()
    try:
        # Determinar el tipo del valor y asignarlo
        new_thing = Thing(id=str(uuid.uuid4()))  # Generar un ID único
        if value.isdigit():  # Es un número entero
            new_thing.ints = int(value)
        elif value.replace('.', '', 1).isdigit():  # Es un número flotante
            new_thing.floats = float(value)
        else:  # Es una cadena
            new_thing.strings = value

        # Guardar en la base de datos
        session.add(new_thing)
        session.commit()
        session.refresh(new_thing)
        return {"id": new_thing.id, "message": "Valor agregado exitosamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al agregar valor: {e}")
    finally:
        session.close()