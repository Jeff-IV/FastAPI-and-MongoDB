from fastapi import  Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
    
class UserDB(User):
    password: str
    
    
users_db = {
            "Jeff-IV": {
                "username": "Jeff-IV",
                "full_name": "Jeferson Garcia Angel",
                "email": "jefeggg20@hisoka.dev",
                "disabled": False,
                "password": "12345"
            }, 
            "Branye123": {
                "username": "Branye23",
                "full_name": "Bryan Garcia Angel",
                "email": "branju13@killua.dev",
                "disabled": True,
                "password": "1555"
            },
            "Papolin": {
                "username": "Papolin",
                "full_name": "Papo Garcia Angel",
                "email": "papolin24@gon.dev",
                "disabled": False,
                "password": "gonlacabra1"
            }
}


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
    
def current_user(token : str = Depends(oauth2)):
    user =  search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details="Usuario no habilitado")
    return user


    
@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_db(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    if form.password != user_db.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Usuario o contraseña incorrectos")
    
    return {"acces_token": user_db.username, "token_type": "bearer"}


@router.get("/users/me")
def me(user: User = Depends(current_user)):
    return user
    