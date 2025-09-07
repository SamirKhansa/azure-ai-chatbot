
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


