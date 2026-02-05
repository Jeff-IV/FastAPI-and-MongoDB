from db.models.user import User

def user_schema(user):
    user_final = {}
    for key in user.keys():
        if key == "_id":
            user_final["id"] = str(user[key])
        #elif key == "age" or key == "phone_number":
        #    user_final[key] = int(user[key])
            
        else:
            user_final[key] = user[key]
            
    return user_final
    
    
def users_schema(list):
    new_user_list = []
    for user in list:
        new_user = user_schema(user)
        new_user_list.append(new_user)
    
    return new_user_list
    
    
        