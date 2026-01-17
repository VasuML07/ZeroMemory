ZeroMemory — Stateless AI Chat App

ZeroMemory is a stateless AI chat application built using Streamlit.
Each message is handled independently — no chat history, no memory, no data storage.

This keeps the app fast, low-cost, and privacy-friendly.

🔗 Live App: https://zeromemory-12.streamlit.app/

What It Does

Takes a user prompt

Sends it to an LLM as a single request

Returns a response

Forgets everything immediately

No sessions. No databases. No stored conversations.

Why Stateless?

Most chat apps keep history, which causes:

Growing token usage

Higher costs

Privacy risks

ZeroMemory avoids all of that by design.

Features

Stateless chat (no memory)

Predictable token usage

Clean Streamlit UI

Secure API key handling

Cloud deployed

Tech Stack

Python

Streamlit

Groq API

Streamlit Cloud

Run Locally
git clone https://github.com/your-username/ZeroMemory.git
cd ZeroMemory
pip install -r requirements.txt


Create a .env file:

GROQ_API_KEY=your_api_key_here


Run the app:

streamlit run app.py

Deployment

Push code to GitHub

Add GROQ_API_KEY in Streamlit Cloud → Secrets

Deploy using app.py

Limitations

No multi-turn conversation

No personalization

No session storage

These are intentional.

What This Shows

LLM API integration

Stateless system design

Cost-aware engineering

Secure deployment basics
