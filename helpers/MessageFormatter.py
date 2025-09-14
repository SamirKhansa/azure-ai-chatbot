
import uuid


def summarize_messages(messages):
    from Services.OpenAiServices import AiReply
    text = ""
    for msg in messages:
        text += msg['role'] + ": " + msg['content'] + "\n"

    # Make a temporary conversation list
    conversation = [{"role": "user", "content": "Please summarize this conversation:\n" + text}]

    
    return conversation



def FormatConversation(conversation):
    history = []
    for msg in conversation:
        if msg["role"] == "user":
            history.append({"user": msg["Content"]})
        elif msg["role"] == "bot":
            if history and "ai" not in history[-1]:
                history[-1]["ai"] = msg["Content"]
            else:
                history.append({"ai": msg["Content"]})
    return history


def SummarizeLongHistory(conversation, max_messages=10):
   
    if len(conversation) <= max_messages:
        return conversation

    
    old_messages = conversation[:-max_messages]
    return conversation

    # summary_text = summarize_messages(old_messages,)
    
    # return [{"role": "system", "content": f"Summary of previous conversation: {summary_text}"}] + conversation[-max_messages:]






def CreateNewId():
    return str(uuid.uuid4())



def chunkText(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks




def AddingRefrencesToAiMessage(results, ai_message):
    unique_sources = set()
    unique_chunks = []
    sources_list = []
    for result in results:
        source = result.get("resource")
        if source not in unique_sources:
            unique_sources.add(source)
            unique_chunks.append(result["Content"])
            if source:  
                sources_list.append(source)
    
    if sources_list:
        return f"{ai_message}\n\nReferences:\n" + "\n".join(sources_list)
    else:
        return ai_message