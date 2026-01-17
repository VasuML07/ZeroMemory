eroMemory — Stateless AI Chat Application

ZeroMemory is a stateless AI-powered chat application built with Streamlit, designed for fast, predictable, and privacy-first AI interactions.

Each user request is processed independently—no chat history, no session memory, no data retention.
This keeps token usage flat, costs predictable, and privacy risks minimal.

🔗 Live App: https://zeromemory-12.streamlit.app/

Overview

Most conversational AI apps retain conversation history to maintain context. While useful, this design introduces:

Growing token usage over time

Higher and unpredictable API costs

Implicit storage of user conversations

Additional session and state complexity

ZeroMemory intentionally avoids all of this.

It follows a single-turn, stateless request model, making it ideal for public demos, cost-sensitive deployments, and privacy-conscious use cases.

Problem Statement

Traditional chat applications often suffer from:

Unbounded context growth

Rising operational costs

Hidden data retention risks

Complex session/state management

These issues become serious blockers when deploying AI apps at scale or in public environments.

Solution Approach

ZeroMemory adopts a stateless architecture:

Each user prompt is sent as a standalone request

No conversation history is stored or reused

No database or session layer is required

Token usage remains constant per interaction

This design prioritizes predictability, simplicity, and security over conversational continuity.

Key Features

Fully stateless chat design

Predictable and capped token usage

Clean, minimal chat-style UI

Secure API key handling via environment variables

Explicit response length limits for cost control

Cloud deployment using Streamlit

Architecture & Design Decisions
Stateless Interaction Model

Each request contains only the current user input.
No previous messages are passed to the model.

Benefits:

Flat token usage

Lower and predictable cost

No context leakage

Easier debugging and reasoning

Explicit Token Control

A hard cap on output length prevents runaway responses and unexpected billing.

Secure Secret Management

API keys are never hard-coded.
Secrets are injected via environment variables or platform-managed secrets.

Minimal Dependency Footprint

Only essential libraries are used to keep the app reliable and easy to maintain.

Tech Stack

Python

Streamlit — UI + hosting

Groq Python SDK — LLM API client

python-dotenv — local environment management

Streamlit Cloud — deployment platform

Project Structure
.
├── app.py              # Main application logic
├── requirements.txt    # Project dependencies
├── .gitignore          # Prevents secret leakage

Setup & Deployment
Local Setup

Clone the repository:

git clone https://github.com/your-username/ZeroMemory.git
cd ZeroMemory


Create a .env file:

GROQ_API_KEY=your_api_key_here


Install dependencies:

pip install -r requirements.txt


Run the application:

python -m streamlit run app.py

Deployment (Streamlit Cloud)

Push app.py and requirements.txt to GitHub

Add GROQ_API_KEY in
Streamlit Cloud → App Settings → Secrets

Deploy using app.py as the entry point

.env is not used in production

Security & Privacy

No user input is stored

No conversation history is retained

API keys are never exposed in source code

Secrets managed via environment variables

Stateless design minimizes data risk by default

Limitations (Intentional Tradeoffs)

No multi-turn conversation memory

No personalization across messages

No persistent user sessions

These are deliberate design choices to guarantee cost control and privacy.

Future Enhancements

Optional system prompt configuration

Streaming responses

Rate limiting and abuse protection

Usage analytics dashboard

Model selection controls

What This Project Demonstrates

This project reflects real-world engineering thinking, including:

Applied LLM integration

Cost-aware system design

Stateless architecture patterns

Secure secret management

Cloud deployment workflows

Writing maintainable, production-ready Python

