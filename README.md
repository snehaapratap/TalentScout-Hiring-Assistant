# 🤖 TalentScout – AI-Powered Hiring Assistant 

An intelligent, context-aware chatbot built using **Streamlit**, **Groq API (LLaMA3)**, and **Docker**, designed to automate the initial candidate screening process for a fictional recruitment agency — **TalentScout**.

This chatbot collects candidate details, dynamically generates relevant technical questions based on their tech stack, and maintains conversational context to simulate a professional hiring assistant.

---

## ✨ Features

### ✅ Core Functionality
- **User-Friendly Chat UI** built with Streamlit
- **Candidate Data Collection**:
  - Full Name, Email, Phone, Experience, Position(s), Location, Tech Stack
- **Dynamic Technical Question Generation** based on tech stack
- **Context Awareness** using a custom conversation manager
- **Fallback Handling** when inputs are unclear
- **Graceful Conversation Exit** (detects "exit", "bye", etc.)

---

## 🧠 Bonus Enhancements

| Feature                     | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| 🧩 Follow-Up Questions      | Based on candidate’s answers, the chatbot asks deeper follow-up questions. |
| ⚡ Groq LLM Integration     | Uses `LLaMA3-70B` via Groq API instead of OpenAI                            |
| 📦 Docker Containerization | Run the entire app inside a Docker container                               |
| 🧼 Duplicate Filter         | Filters repeated or hallucinated questions                                 |
| 🧪 Simulated Candidate DB   | Option to store simulated responses locally                                |

---

## 🛠️ Tech Stack

| Layer         | Technology              |
|---------------|--------------------------|
| UI            | Streamlit                |
| LLM Backend   | Groq API (LLaMA3)        |
| Prompt Design | Custom prompt templates  |
| Data Storage  | Simulated JSON (DB ready)|
| Container     | Docker                   |

---

## 📂 Project Structure

```

TalentScout-Hiring-Assistant/
│
├── app.py                      # Main Streamlit App
├── requirements.txt
├── .env                        # Groq API keys
├── Dockerfile                  # Docker container definition
├── README.md
│
├── utils/
│   ├── prompt.py     # LLM prompt generation logic
│   └── context_handler.py      # Tracks conversation state
│
├── backend/
│   └── llm_handler.py  # groq-based functions
│
├── .dockerignore

````

---

## ⚙️ Setup Instructions (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/snehaapratap/TalentScout-Hiring-Assistant.git
cd TalentScout-Hiring-Assistant
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` File

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

### 4. Run Locally

```bash
streamlit run app.py
```

Then open: [http://localhost:8501](http://localhost:8501)

---

## 🐳 Docker Setup

### 1. Build Docker Image

```bash
docker build -t talentscout-assistant .
```

### 2. Run the Container

```bash
docker run --env-file .env -p 8501:8501 talentscout-assistant
```

> The app will be available at: [http://localhost:8501](http://localhost:8501)


---

## 📊 Prompt Design Strategy

* **Role-Based Prompting**: Separates system, user, and assistant roles to guide behavior.
* **Tech Stack Mapping**: Dynamically parses tech keywords to generate questions.
* **Clarity Constraints**: Prompts instruct LLM not to hallucinate or repeat.
* **Follow-Up Design**: Injects question-answer pairs to prompt relevant follow-ups.

---

## 🧪 Challenges & Solutions

| Challenge                | Solution                                                           |
| ------------------------ | ------------------------------------------------------------------ |
| Question repetition      | Added filtering + prompt constraints                               |
| No follow-up interaction | Built context manager to track QA flow and ask follow-up questions |
| LLM hallucinations       | Added fallback messages + clean prompt design                      |
| LLM response delay       | Chose Groq API (LLaMA3) for ultra-low latency                      |

---

## 🔐 Data Privacy Considerations

* ❌ No real user data is stored or shared
* ✅ Simulated data used for demo purposes
* 🔐 Environment variables stored securely via `.env`
* 📜 Complies with basic GDPR demo standards
