# Chatbot Architecture Documentation

---

## 1. Overview
This document describes the architecture, data flow, and setup instructions for the Azure OpenAI chatbot implementation. The chatbot is capable of:

- Maintaining persistent conversation history in Cosmos DB

- Retrieving information from documents using RAG (Retrieval-Augmented Generation)

- Operating with a specific role or prompt to guide responses

- Being deployed to Azure for cloud accessibility

---

## 2. Resources Used
| Resource | Description |
|----------|-------------|
| **Resource Group** | A container that holds all project resources, making them easier to manage and organize. |
| **Function App** | Hosts Python code, accessible via HTTP requests, allowing the chatbot to run independently of a local machine. |
| **CosmosDB** | Hosts chat history that is divided by every user unique session id. Furthermore, this database also hosts the documents with their embeddings.   |
| **Azure AI Foundaty Resource** | Contains the GPT-4o deployment, gpt text-embedding and handles AI processing. |
| **GPT-4o Deployment** | AI model that generates responses based on user input and developer-defined prompts. |
| **text-embedding-3-small** | AI model that generates an embedding  based on the text provided. |


---

## 3. Architecture Diagram
![Chatbot Architecture](/Assets/V1.1.png)

---

## 4. Data Flow and Component Interactions
1. **User → Function App:** The user sends an HTTP request containing their message. 
2. **Function App -> CosmosDb Resource:**  Retreives the chunks of documents from the database and the chat history if it exsists from the user.
3. **Function App → Azure AI Foundary Resource:** The Function App hosts the code, including prompts that instruct GPT-4o how to respond. Furhtermore, Azure AI Foundary has also deployed a model called text-embedding-3-small to turn text into embedding.  
4. **Azure AI Foundary → text-embedding-3-small:** text-embedding-3-small processes the user message and transforms it into an embedding to be used with the embedding of the chunks. This model is also used when a new document is saved, divided into chunks, turned into an embedding and saved to CosmosDB.  
5. **Azure AI Foundary**: After retriving the embedding of the user question, the model then uses cosine similarity to provide GPT 4o model the top 3 most relavent chunks of documents that could contain the ansewer.
6. **Azure AI Foundary → GPT-4o Deployment:** GPT-4o processes the user message, provided chunks of document and prompt to generate a response.  
7. **GPT-4o Deployment → Function App:** The generated response is sent back to the Function App.
8. **GPT-4o Deployment → Chosmos Db:** The generated response is saved in Cosmos DB chatHistory of the user .  
9. **Function App → User:** The Function App returns the response to the user immediately.

---
## 5.Features Implemented
- Persistent chat history stored in Cosmos DB

- Clear conversation or session restart command support

- Prompt customization for system role (topic-specific responses)

- RAG knowledgebase for document-based answers

- Deployed solution in Azure for live access
--

## 6. Future Updates
- Enhanced conversational flows and multi-turn context summarization

- Expanded knowledgebase with more documents

- Integration of multi-modal input (images, audio)

- Analytics dashboard to monitor chatbot usage

---

## 7. Setup Instructions

### Prerequisites
- Python 3.10+  
- Azure Portal account  
- Azure CLI  
- Azure Functions Core Tools  
- Azure Resource Group (via VS Code)  
- Git  

### Azure Portal Setup
1. Choose a subscription plan.  
2. Create a **Resource Group**. Ensure all resources are in the same region.  
3. Create an **Azure OpenAI resource** in the same Resource Group and region.  
4. Open **Azure AI Foundry** to deploy the GPT-4o model and text-embedding-3-small.  
6. Once GPT-4o and text-embedding-3-small is deployed, copy the **key, endpoint, and model version**.  
7. Paste these values into Visual Studio Code to connect the model.
8. Create a CosmosDB resource, set the resource region similar to the region of the Resource group.
9. Create two containers in the database. The first container name should be Documents with partition key /id and the second container name is Sessions with partition key /sessions

### Local Setup
1. Clone the repository:
```
git clone https://github.com/SamirKhansa/azure-ai-chatbot
cd azure-ai-chatbot

```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run the function locally:
```
func start
```
4. Test the function using CLI (curl) or Postman with the endpoint provided by func.

## 7. API Configuration

| Item | Details |
|------|---------|
| **Deployed Endpoint** | `https://<your-function-app>.azurewebsites.net/api/ChatbotFunction` |
| **Local Endpoint** | `http://localhost:7071` (provided by `func start`) |
| **Method** | POST |
| **Headers** | `Content-Type: application/json` |
| **Response Example** | JSON object containing the chatbot reply |
| **Error Handling** | **User Input Error:** Invalid or missing JSON message <br> **System Error:** Backend issues |

### Usage Examples

**Using curl**
```
curl -X POST "https://<your-function-app>.azurewebsites.net/api/ChatbotFunction" \
  -H "Content-Type: application/json" \
  -d '{"message": ""message": "can you tell me a nice fact Kings Gambit?"", "first_interaction": true}'
```
**Expected Response**
```
{
  "reply": "Certainly! Here's a fascinating fact about the King’s Gambit:\n\nThe King’s Gambit was famously described as \"the most beautiful of all gambits\" by Wilhelm Steinitz, the first World Chess Champion. Its daring nature and romantic character made it the hallmark of the 19th-century Romantic Era of chess. In fact, one of the most celebrated games in chess history, Adolf Anderssen's \"Immortal Game\" (1851), featured the King’s Gambit. Anderssen sacrificed multiple pieces, including both rooks and his queen, to deliver a stunning checkmate—showcasing the opening's immense attacking potential and creative brilliance. \n\nEven today, the King’s Gambit is admired for its boldness and ability to create memorable, tactical battles!"
}
```
### 8. Screenshots
- AI response
![AI response](/Assets/KingsGambitFact.JPG)
- User Input Irrelivant information
![Irrelivant Information](/Assets/Speciality.JPG)
- User Input Error
![User Error](/Assets/UserError.JPG)
- System Error
![System Error](/Assets/SystemError.JPG)

