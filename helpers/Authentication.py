import bcrypt



def CheckPassword(user, password):
    stored_hashed_password = user.get("password")
    if not stored_hashed_password:
         raise ValueError("User Password not set")
    
    if not bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password.encode("utf-8")):
        raise ValueError("Invalid email or password")
    return stored_hashed_password


def getSignInParameter(req_body):
    role=req_body.get("role")
    name=req_body.get("name")
    email=req_body.get("email")
    password=req_body.get("password")
    password_confirmation = req_body.get("password_confirmation")

    if not all([name, email, password, password_confirmation]):
        raise ValueError("Error all feilds are required")
    if(password !=password_confirmation):
        raise ValueError("Password and Confirm Password do not match")
    
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return role, name, email, hashed_password

