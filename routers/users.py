from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/user", tags=["user"], responses={404: {"message" : "No encontrado"}})
router2 = APIRouter(prefix="/users", tags=["users"], responses={404: {"message" : "No encontrado"}})

#inicializar servidor con fastapi dev users.py  o con  uvicorn users:app --reload

#Entidad User
class User(BaseModel):
    id : int
    name : str
    surname : str
    age : int

users_list = [
                User(id = 1, name = "Jeff", surname = "IV", age = 22), 
                User(id = 2, name = "Papo", surname = "Garcia", age = 24),
                User(id = 3, name = "Branye", surname = "Angel", age = 25)
            ]


@router2.get("/JSON")
def users_JSON():
    return [
                { "name": "Jeff", "surname":"IV", "age":22 },
                {"name": "Papo", "surname":"Garcia", "age":24},
                {"name": "Branye", "surname": "Angel", "age":25}
            ]
    
@router2.get("/")
def users_object():
    return users_list

# Path
@router.get("/{id}")
def user_id(id : int ):
    user = search_user(id) 
    if user == False: 
        raise HTTPException(status_code = 404, detail = "El usuario no existe")
    else: 
        return search_user(id)
        
# Query
@router.get("/")
def user_id_query(id : int ):
    user = search_user(id) 
    if user == False: 
        raise HTTPException(status_code = 404, detail = "El usuario no existe")
    else: 
        return search_user(id)


## METODOS POST 
@router.post("/", status_code=201, response_model=User)
def new_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code = 409, detail = "El usuario ya existe")
        #return { "error": f"El usuario con id: {user.id} ya existe."}
    else:
        users_list.append(user)
        return user
    

## METODOS PUT
@router.put("/", status_code=201, response_model=User)
def update_user(user: User):
    if type(search_user(user.id)) == User:
        for index, saved_user in enumerate(users_list):          
            if user.id == saved_user.id:
                users_list[index] = user
                return user           
    else: 
        raise HTTPException(status_code = 404, detail = "El usuario no existe")

    
## METODOS DELETE
@router.delete("/{id}", status_code=200, response_model=User)
def delete_user(id: int):
    if type(search_user(id)) == User:
        for index, saved_user in enumerate(users_list):          
            if id == saved_user.id:
                del users_list[index]
                return saved_user           
    else: 
        raise HTTPException(status_code = 404, detail = "El usuario no existe")
    
    
    
    

   
# Funciones globales
def search_user(id : int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return False
    
