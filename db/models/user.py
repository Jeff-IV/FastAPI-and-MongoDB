from pydantic import BaseModel
from typing import Optional

#def id_definer():
#    base = "US-"
#    number_base = 0
#    
#    def iterador():
#        nonlocal number_base 
#        number_base += 1
#        return f"{base}{number_base}"
#
#    return iterador


class User(BaseModel):
    id: Optional[str] = None
    username: str
    name: str
    surname: str
    age: int
    url: str
    email: str
    phone_number: int
    
