
from helpers.MessageFormatter import CreateNewId, SummarizeLongHistory


def SaveConversation(container, document_id, session_id, conversation):
    container.upsert_item({
        "id": document_id,
        "sessionId": session_id,
        "messages": conversation
    })


def ConversationHistory(session_id, container, user_message):
    query = f"SELECT * FROM c WHERE c.sessionId = '{session_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    if items:
        conversation = items[0]["messages"]
        doc_id = items[0]["id"]
    else:
        conversation = []
        doc_id = CreateNewId()
    
    conversation.append({"role": "user", "Content": user_message})
    conversation = SummarizeLongHistory(conversation, max_messages=10)

    return conversation,doc_id




def PromoteDenoteUsers(UserContainer, emails, Role):
    try:
        print("1111111111111111111111111111")
        user = UserContainer.read_item(item=emails, partition_key=emails)
        # print("User found:", user)
        print("22222222222222222222222222222222222")

        # Update the role
        user["role"] = Role
        print("333333333333333333333333333333333333")

        # Replace the item in CosmosDB
        UserContainer.replace_item(item=emails, body=user)
        print("User role updated.")

        return f"The user has successfully been set to {Role}"

    
        
    except Exception as e:
        print("Unexpected error:", e)
        return f"Failed to update user role: {e}"

def DeleteUser(UserContainer, email):
    UserContainer.delete_item(item=email)
    return "The User has sucessfully been deleted!!"

