# Chatbot Architecture Documentation

## 1. Overview
This document will explain the flow and data flow for the Azure OpenAI chatbot implementation. 

## 2. Resources Used:
- **Resource Group**:A Resource Group is like a folder that contains all of the resources for a project, making them easier to manage and organize together.
- **Function App**: Hosts Python code, making it accessible via HTTP requests at any time. This allows the chatbot running on a machine without depending on a local machine.
- **Azure OpenAI Resource**: This resource contains GPT-4o deployment and handles other AI processing. 
-**GPT-4o Deployment**: This is an AI model generates responses when giving a question and a prompt through the provided python code.



## 3. Architecture Diagram
![Chatbot Architecture](/Assets/Architecture%20Diagram.png)

## 4. Data Flow and Component Interactions
1. **User->Function App**: Users will send a HTTP request that is going to contain their message for the function app chatbot.

2. **Function App -> Azure OpenAI Resource**: The Function App inside a resource group will host our code. In the code, there will be a prompt telling OpenAI the structure in which it should respond.

3. **Azure OpenAI Resource -> GPT-4o Deployment**: In this stage the GPT 4o model is going to process the message from the user and the prompt form the developer and is going to generate a response.
4. **GPT-4o Deployment-> Function App**: The message that the GPT 4o model generated is going to be returned to the Function App.
5. **Function App -> User**: Once the generated response is returned to the Function App, the program will immediatly return the response to the user.

## 5. Future Updates
This diagram and documentation represent the current basic chatbot setup. In the future, new features are going to be added such as persistent chat history or enhanced conversational flows. This document and diagram will be updated accordingly.


