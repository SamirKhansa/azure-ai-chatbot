def FormatMessage(Greetings,aiMessage):
    if(Greetings):
        return f"{Greetings}\n{aiMessage}"
    else:
        return aiMessage
    


def GreetingMessage(req_body):
    WELCOME_MESSAGE = "Hello! I am your chatbot. Type your message or 'exit' to end the conversation."
    if req_body.get("first_interaction", False):
        greeting = WELCOME_MESSAGE
    else:
        greeting = None

