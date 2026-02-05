from fastapi import  Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 1 # 1 minuto
SECRET = "cb96dedb8610686bc06f8502f6440b9f418acc4037439e3c3982cc573b50863b"


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


## Clases

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
    
class UserDB(User):
    password: str
    
    
## Base de datos ficticia con contraseñas encriptadas con algoritmo de hash
users_db = {
            "Jeff-IV": {
                "username": "Jeff-IV",
                "full_name": "Jeferson Garcia Angel",
                "email": "jefeggg20@hisoka.dev",
                "disabled": False,
                "password": "$2a$12$Uedvd3hbkxbhSGDhnRdUMe5LGogLKvhwVSOtOceT.Oqygk2KPYDHK"
            }, 
            "Branye123": {
                "username": "Branye23",
                "full_name": "Bryan Garcia Angel",
                "email": "branju13@killua.dev",
                "disabled": True,
                "password": "$2a$12$U7IYxR11YRpCn4CTUBorgueDjluB93jNPCZqNFZ1rjbwZ4qxjNmWm"
            },
            "Papolin": {
                "username": "Papolin",
                "full_name": "Papo Garcia Angel",
                "email": "papolin24@gon.dev",
                "disabled": False,
                "password": "$2a$12$1RWWhHy/AKWUWbhr2kOf/.XvOpUZQQtCJNUyzi84N5L8016LHb8iW"
            }
}


## Funciones globales
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    else: return False
    
def search_user(username: str):
    if username in users_db:
        user = users_db[username]
        user.pop("password")
        return User(**user)
    else: return False
    
    
def auth_user(token : str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception    
        
    except JWTError:
        raise exception

    return search_user(username)
    

def current_user(user : User = Depends(auth_user)):

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details="Usuario no habilitado")
    return user



# Metodos post    
@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_db(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
    
    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Usuario o contraseña incorrectos")
    
    
    
    access_token = {
        "sub": user_db.username, 
        "exp": datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION),
    }
    
    return {"acces_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}



@router.get("/users/me")
def me(user: User = Depends(current_user)):
    return user
    


 