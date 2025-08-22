# Chatbot Architecture Documentation

---

## 1. Overview
This document describes the architecture, data flow, and setup instructions for the Azure OpenAI chatbot implementation.

---

## 2. Resources Used
| Resource | Description |
|----------|-------------|
| **Resource Group** | A container that holds all project resources, making them easier to manage and organize. |
| **Function App** | Hosts Python code, accessible via HTTP requests, allowing the chatbot to run independently of a local machine. |
| **Azure OpenAI Resource** | Contains the GPT-4o deployment and handles AI processing. |
| **GPT-4o Deployment** | AI model that generates responses based on user input and developer-defined prompts. |

---

## 3. Architecture Diagram
![Chatbot Architecture](/Assets/Architecture%20Diagram.png)

---

## 4. Data Flow and Component Interactions
1. **User → Function App:** The user sends an HTTP request containing their message.  
2. **Function App → Azure OpenAI Resource:** The Function App hosts the code, including prompts that instruct GPT-4o how to respond.  
3. **Azure OpenAI Resource → GPT-4o Deployment:** GPT-4o processes the user message and developer prompts to generate a response.  
4. **GPT-4o Deployment → Function App:** The generated response is sent back to the Function App.  
5. **Function App → User:** The Function App returns the response to the user immediately.

---

## 5. Future Updates
This documentation represents the current basic chatbot setup. Future enhancements may include:  
- Persistent chat history  
- Enhanced conversational flows  
- Updated diagrams and instructions

---

## 6. Setup Instructions

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
4. Open **Azure AI Foundry** to deploy the GPT-4o model.  
5. If in Europe, choose **Sweden** as the deployment region.  
6. Once GPT-4o is deployed, copy the **key, endpoint, and model version**.  
7. Paste these values into Visual Studio Code to connect the model.

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
  -d '{"message": "Tell me a fun fact about space?", "first_interaction": true}'
```
**Expected Response**
```
{
  "reply": "Sure! Here's a fascinating fact about space: There are more stars in the universe than grains of sand on all the beaches on Earth! Astronomers estimate that the observable universe contains around **200 billion trillion stars** (that's 2 followed by 23 zeros). Each star could potentially host its own planetary system, making the universe unimaginably vast and full of possibilities. 🌌✨"
}
```
### 8. Screenshots
- AI response
![AI response](/Assets/AI%20response.JPG)
- User Input Error
![User Error](/Assets/UserError.JPG)
- System Error
![System Error](/Assets/SystemError.JPG)

