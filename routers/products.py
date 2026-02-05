from fastapi import APIRouter

router = APIRouter(prefix="/products", tags= ["products"], responses={404: {"message" : "No encontrado"}})

products_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/")
def products():
    return products_list

@router.get("/{index}")
def product_id(index: int):
    return products_list[index]