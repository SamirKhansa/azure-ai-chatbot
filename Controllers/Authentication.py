from helpers.ErrorHandling import UserMessageError, SystemError
from Services.OpenAiServices import ReplyToAdmin,  SendReply
from Services.CosmosDbServices import GetUser, GetAllDocuments, GetAllUsers, CreateUser
from helpers.Authentication import CheckPassword, getSignInParameter
import uuid




def SignUp(UserContainer, req_body):
    role, name, email, hashed_password= getSignInParameter(req_body)
    user={
        "id": str(uuid.uuid4()),
        "name": name,
        "email":email,
        "password":hashed_password.decode("utf-8"),
        "role": "User"
    }
    CreateUser(UserContainer, user)
    return "SignUp is Sucessfull"


def LogIn(UserContainer, DatabaseContainer,req_body, search_client):
    email=req_body.get("email")
    password=str(req_body.get("password"))

    if not all([email, password]):
        return UserMessageError("Error: Email and Password are required", 400)
    print("Finding User")
    user=GetUser(UserContainer, email)
    

    print("Cheking Password ",user)
    CheckPassword(user, password)
   
    
    
    role=user.get("role")
    response_data = {
        "message": "Login successful",
        "Status":200,
        "role": role,
        "userId": user.get("UserId"),
    }
   
    if role == "Admin":

        print("Getting All users")
        all_users = GetAllUsers(UserContainer)
        print("Getting all documents")
        all_documents = GetAllDocuments(DatabaseContainer)
        print("Theoratically it should work!")
       
        response_data["adminData"] = {
            "users": all_users,
            "documents": all_documents
        }
        
        
    return ReplyToAdmin(response_data)
    
    