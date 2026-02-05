from fastapi import FastAPI
from routers import products, users, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router) # "/products"
app.include_router(users.router) # "/user"
app.include_router(users.router2)# "/users"
app.include_router(jwt_auth_users.router) # "/login"
app.include_router(basic_auth_users.router) # "/login"
app.include_router(users_db.router) # "/userdb"
app.include_router(users_db.router2) # "/usersdb"
app.mount("/static", StaticFiles(directory="static"), name="static") # montando un recurso estático



@app.get("/")
def root():
    return "Hola FastAPI!"


@app.get("/url")
def url():
    return { "url_curso" : "https://mourdev.com/python" }