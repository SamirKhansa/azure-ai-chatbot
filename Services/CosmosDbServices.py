def SaveConversation(container, document_id, session_id, conversation):
    container.upsert_item({
        "id": document_id,
        "sessionId": session_id,
        "messages": conversation
    })