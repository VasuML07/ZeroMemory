# 🧠 ZeroMemory  
### Stateless AI Chat Application

ZeroMemory is a stateless AI chat application built using Streamlit.

Each request is processed independently — no conversation history, no memory, no stored data.

The system is intentionally designed to be fast, cost-efficient, and privacy-focused.

---

## 🔗 Live Application

🌐 https://zeromemory-12.streamlit.app/

---

## ⚙️ What It Does

- Accepts a user prompt  
- Sends a single request to an LLM  
- Returns the generated response  
- Immediately discards all context  

No sessions.  
No databases.  
No stored conversations.

---

## 🧠 Why Stateless Design?

Most chat applications store conversation history, which leads to:

- Increasing token usage  
- Higher API costs  
- Growing privacy risks  

ZeroMemory avoids these by design.

Each request is isolated and predictable in compute usage.

---

## 🚀 Features

- Stateless request handling  
- Predictable token consumption  
- Minimal Streamlit UI  
- Secure API key management  
- Cloud deployment ready  

---

## 🛠 Tech Stack

### 💻 Core Language
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

---

### 🌐 Framework
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

---

### 🤖 LLM Integration
![Groq](https://img.shields.io/badge/Groq%20API-LLM%20Inference-black?style=flat-square)

---

### ☁ Deployment
![Streamlit Cloud](https://img.shields.io/badge/Streamlit%20Cloud-Deployed-FF4B4B?style=flat-square)

---

## 📁 Project Structure

ZeroMemory/
│
├── app.py
├── requirements.txt
└── README.md


---

## ⚙️ Run Locally

### 📥 Clone Repository

```bash
git clone https://github.com/your-username/ZeroMemory.git
cd ZeroMemory
📦 Install Dependencies
pip install -r requirements.txt
🔐 Create Environment File
Create a .env file:

GROQ_API_KEY=your_api_key_here
▶ Run Application
streamlit run app.py
☁ Deployment
Push project to GitHub

Add GROQ_API_KEY inside Streamlit Cloud → Secrets

Deploy using app.py

⚠ Limitations (By Design)
No multi-turn conversation

No personalization

No session storage

These constraints are intentional to preserve stateless behavior.

🎯 What This Demonstrates
LLM API integration

Stateless system architecture

Cost-aware engineering design

Secure environment variable handling

Cloud deployment fundamentals

ZeroMemory prioritizes simplicity, privacy, and predictable resource usage over conversational depth.
