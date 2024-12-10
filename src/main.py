from fastapi import Depends, FastAPI, HTTPException, Header, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from src.routers.routers import app as app_router
from src.utils.http_erro_handler import HttpErrorHandler
import os
from jose import jwt
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker





app = FastAPI()

oauth = OAuth2PasswordBearer(tokenUrl='token')

users = {
    'a': {
        'username': 'a',
        'password': 'p'
    },
    'b': {
        'username': 'b',
        'password': 'p'
    }
}

def get_headers(
    access_token: Annotated[str | None, Header()] = None,
    user_rol: Annotated[str | None, Header()] = None
        ):
    if access_token != 'secret':
        raise HTTPException("No autorizado")
    return {
        'access_token': access_token,
        'user_rol': user_rol
    }
    

def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, 'secrect', algorithm='HS256')
    return token

def decode_token(token: Annotated[str, Depends(oauth)]) -> dict:
    data = jwt.decode(token, 'secrect', algorithms=['HS256'])
    user = users.get(data['username'])
    return user



# uso de starlet para manejar errores mendiante starlet
app.add_middleware(HttpErrorHandler)

# manejo de errores mediante fastapi
'''
@app.middleware('http')
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    try:
        return await call_next(request)
    except Exception as e:
        content = f"exc: {str(e)}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content=content, status_code=status_code)
'''

# agrega al path de la app las direcciones staticas y templates
static_path = os.path.join(os.path.dirname(__file__), 'statics/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

# monta los staticos y crea los templates
app.mount('/statics', StaticFiles(directory=static_path), 'statics')
templates = Jinja2Templates(directory=templates_path)

# modificando la ruta de docs
app.title = "Mi app"
app.version = "v0.1" 

# devuelve un una respuesta de templates copulado por /templates/index.html
@app.get('/home', tags=['Home'])
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'message': 'Welcome'})


@app.post('/token')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user =  users.get(form_data.username)
    if not user or form_data.password != user['password']:
        raise HTTPException(status_code=400, detail="Login error")
    token = encode_token({ 'username': user['username'] })
    return { 'access_token': token }

@app.get('/user/profile')
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user


@app.get('/headers')
def headers(request: Request, response: Response, headers: Annotated[dict, Depends(get_headers)]):
    response.headers['user_status'] = 'enable'
    print(request.headers)
    return {
        'access_token': headers['access_token'],
        'user_rol': headers['user_rol']
    }
    
@app.get('/')
def root(response: Response):
    response.set_cookie(key="username", value="cooo")
    return 'welcome'

app.include_router(router=app_router)