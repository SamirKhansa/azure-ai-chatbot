
import uuid
from PyPDF2 import PdfReader

def summarize_messages(messages, client):
    from Services.OpenAiServices import AiReply
    # Convert messages to a single conversation string
    text = ""
    for msg in messages:
        text += msg['role'] + ": " + msg['content'] + "\n"

    # Make a temporary conversation list
    conversation = [{"role": "user", "content": "Please summarize this conversation:\n" + text}]

    summary = AiReply(client=client, conversation=conversation)
    return summary



def FormatConversation(conversation):
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


def SummarizeLongHistory(conversation, max_messages=10):
   
    if len(conversation) <= max_messages:
        return conversation

    
    old_messages = conversation[:-max_messages]
    summary_text = summarize_messages(old_messages)
    
    return [{"role": "system", "content": f"Summary of previous conversation: {summary_text}"}] + conversation[-max_messages:]


def ConversationHistory(session_id, container, user_message):
    query = f"SELECT * FROM c WHERE c.sessionId = '{session_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    if items:
        conversation = items[0]["messages"]
        doc_id = items[0]["id"]
    else:
        conversation = []
        doc_id = CreateNewId()
    
    conversation.append({"role": "user", "content": user_message})
    conversation = SummarizeLongHistory(conversation, max_messages=10)

    return conversation,doc_id



def CreateNewId():
    return str(uuid.uuid4())

def ExtractTextFromPDF(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunkText(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks