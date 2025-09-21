from helpers.ErrorHandling import UserMessageError, SystemError
from Services.OpenAiServices import ReplyToAdmin,  SendReply
import uuid
import bcrypt



def SignUp(UserContainer, req_body):
    role=req_body.get("role")
    name=req_body.get("name")
    email=req_body.get("email")
    password=req_body.get("password")
    password_confirmation = req_body.get("password_confirmation")
    if not all([name, email, password, password_confirmation]):
        return UserMessageError("Error all feilds are required", 400)
    if(password !=password_confirmation):
        return UserMessageError("Password and Confirm Password do not match", 400)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user={
        "id": str(uuid.uuid4()),
        "name": name,
        "email":email,
        "password":hashed_password.decode("utf-8"),
        "role": role
    }
    UserContainer.create_item(body=user)
    return SendReply("SignUp is Sucessfull")


def LogIn(UserContainer, req_body, search_client):
    email=req_body.get("email")
    password=str(req_body.get("password"))
    print(11)
    if not all([email, password]):
        return UserMessageError("Error: Email and Password are required", 400)
    query = "SELECT * FROM c WHERE c.email=@email"
    params = [{"name": "@email", "value": email}]
    users = list(UserContainer.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))
    if not users:
        return UserMessageError("Invalid email or password", 401)
    user=users[0]
    stored_hashed_password = user.get("password")
    print(22)

    if not stored_hashed_password:
        return SystemError("User password not set")
    print(33)
    
    if not bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password.encode("utf-8")):
        return UserMessageError("Invalid email or password", 401)
    role=user.get("role")
    response_data = {
        "message": "Login successful",
        "Status":200,
        "role": role,
        "userId": user.get("UserId"),
    }
    print(44)
    if role == "Admin":
        print(55)
        
        all_users = list(UserContainer.query_items(
            query="SELECT c.name, c.email, c.role FROM c",
            enable_cross_partition_query=True
        ))
        print(55)
        
        all_documents = [
            {"Name": doc.get("Name"), "resource": doc.get("resource"), "Type":doc.get("Type"), "UploadedBy":doc.get("UploadedBy")}
            for doc in search_client.search(search_text="*")
        ]
        print(77)
        print(all_documents)

        response_data["adminData"] = {
            "users": all_users,
            "documents": all_documents
        }
        print(88)
        
    return ReplyToAdmin(response_data)
    
    