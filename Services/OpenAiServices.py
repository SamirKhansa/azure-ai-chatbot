
import json
import azure.functions as func

def AiReply(client, user_message):
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=400,
        temperature=0.7,
        top_p=0.9
    )

    return response.choices[0].message.content.strip()


def ReplyToUser(ai_message):
    return func.HttpResponse(
        json.dumps({"response": ai_message}),
        status_code=200,
        mimetype="application/json"
    )


    