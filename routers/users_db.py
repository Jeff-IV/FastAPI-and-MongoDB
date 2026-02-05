from fastapi import APIRouter, HTTPException
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId


router = APIRouter(prefix="/userdb", tags=["userdb"], responses={404: {"message" : "No encontrado"}})
router2 = APIRouter(prefix="/usersdb", tags=["usersdb"], responses={404: {"message" : "No encontrado"}})

#inicializar servidor con fastapi dev users.py  o con  uvicorn users:app --reload



    
@router2.get("/", response_model=list[User])
def users_object():
    bd_users_list =  db_client.users.find()
    
    return users_schema(bd_users_list)

# Path
@router.get("/{id}")
def user_id(id : str ):
    try:
        user =  search_user("_id", ObjectId(id))
        if user != False:
            return user
        raise HTTPException(status_code = 404, detail = "El usuario no existe")
    except:
        raise HTTPException(status_code = 400, detail = "id inválido")
 
        
# Query
@router.get("/")
def user_id_query(id : str ):
    try:
        user =  search_user("_id", ObjectId(id))
        if user != False:
            return user
        raise HTTPException(status_code = 404, detail = "El usuario no existe")
    except:
        raise HTTPException(status_code = 400, detail = "_id inválido")


## METODOS POST 
@router.post("/", status_code=201, response_model=User)
def new_user(user: User):
    
    if search_user("username" , user.username) != False:
        raise HTTPException(status_code = 409, detail = "El usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]
    
    id = db_client.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    
    return new_user
    
    
    
    

## METODOS PUT
@router.put("/", status_code=201, response_model=User)
def update_user(user: User):
    try:   
        user_dict = dict(user)
        del user_dict["id"]   
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    
    except:
        raise HTTPException(status_code=400, detail= "Eror al buscar al usuario")
    
    return search_user("_id", ObjectId(user.id))
    
    
## METODOS DELETE
@router.delete("/{id}", status_code=200, response_model=User)
def delete_user(id: str):
    try:
        user = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
        
        if not user:
            raise HTTPException(status_code = 404, detail = "El usuario no existe")
        
        return user
    
    except:
        raise HTTPException(status_code = 400, detail = "id inválido")
    
    

   
# Funciones globales
def search_user(field : str, value):
    try:
        user = db_client.users.find_one({field: value})
        if user != None:
            return User(**user_schema(user))
        return False
    except:
        raise HTTPException(status_code=400, detail= "Eror al buscar al usuario")
    



