

from helpers.ErrorHandling import UserMessageError
from Services.OpenAiServices import AiReply, ReplyToChat, TextEmbedding, SendReply
from helpers.MessageFormatter import FormatConversation, CreateNewId, AddingRefrencesToAiMessage, PromptForImageGeneration
from Services.CosmosDbServices import SaveConversation, ConversationHistory
from Services.AiSearchServices import RetreiveRelevantChunks
from Services.SpeechAPI import text_to_speech, speech_to_text









def ChatBot(req_body,EmbeddingClient, GPT4oClient, speechClient, search_client, ChatContainer):
    
    
    user_message = req_body.get("message")
    audio_base64 = req_body.get("audioBase64")
    session_id = req_body.get("sessionId")
    
    if audio_base64:
        print("Their is an audio")
        user_message=speech_to_text(audio_base64, speechClient)
        
    if not user_message:
        return UserMessageError("Please provide a 'message' in JSON",400)

    if user_message.strip().lower() in ['exit', 'quit', 'bye']:
        return SendReply("Goodbye! Have a nice day 🙂")


    if not session_id:
        session_id = CreateNewId()

    print("I am the user Message ",user_message)
    conversation, document_id = ConversationHistory(session_id=session_id, container=ChatContainer, user_message=user_message)
    
    print("Problem is not in cosmos DB")
    query_embedding = TextEmbedding(EmbeddingClient=EmbeddingClient, message=user_message)
    print("Problem is not in text embedding")
    
    results = RetreiveRelevantChunks(search_client=search_client,query_embedding=query_embedding, top_k=3)
    print("Problem is not in AI Search")
    
    
    retrieved_texts = [result["Content"] for result in results]
    
    context_prompt = "\n\n".join(retrieved_texts)
    

    ai_message = AiReply(client=GPT4oClient, conversation=conversation, context=context_prompt, tools=PromptForImageGeneration())
    print("5555")
    print("I am in the chat page")
    print(ai_message["type"])
    print("type was printed")
    
    if(ai_message["type"]!="image"):
        print("666666")
        audio_base64=text_to_speech(ai_message["Content"], speechClient)
        print("77777")
        ai_message2=AddingRefrencesToAiMessage(results=results, ai_message=ai_message["Content"])
        
        conversation.append({"role": "bot", "Content": ai_message2})
    
        SaveConversation(ChatContainer, document_id, session_id, conversation)
        
    
        conversation_history = FormatConversation(conversation)
        return ReplyToChat( session_id, conversation_history,type="text",audio_base64=audio_base64, ai_message=ai_message2)
        
    conversation_history=conversation
    return ReplyToChat( session_id, conversation_history, type="Image", Image_url=ai_message["url"], ai_message=ai_message["text"])