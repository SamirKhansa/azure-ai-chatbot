from Services.OpenAiServices import AiReply
import uuid


def summarize_messages(messages, client):
   
    text = ""
    for msg in messages:
        text += msg['role'] + ": " + msg['content'] + "\n"
    
    
    summary = AiReply(client=client, user_message="Please summarize this conversation:\n" + text)
    
    
    return summary


def format_conversation(conversation):
    history = []
    for msg in conversation:
        if msg["role"] == "user":
            history.append({"user": msg["content"]})
        elif msg["role"] == "bot":
            if history and "ai" not in history[-1]:
                history[-1]["ai"] = msg["content"]
            else:
                history.append({"ai": msg["content"]})
    return history


def manage_context(conversation, max_messages=10):
   
    if len(conversation) <= max_messages:
        return conversation

    
    old_messages = conversation[:-max_messages]
    summary_text = summarize_messages(old_messages)
    
    return [{"role": "system", "content": f"Summary of previous conversation: {summary_text}"}] + conversation[-max_messages:]


def ConversationHistory(session_id, container):
    query = f"SELECT * FROM c WHERE c.sessionId = '{session_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    if items:
        conversation = items[0]["messages"]
        doc_id = items[0]["id"]
    else:
        conversation = []
        doc_id = CreateNewId()
    return conversation,doc_id



def CreateNewId():
    return str(uuid.uuid4())