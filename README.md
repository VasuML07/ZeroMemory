ZeroMemory

ZeroMemory is a lightweight, stateless AI chat application built with Streamlit.
Each user query is processed independently, with no conversation history stored, ensuring predictable behavior, controlled token usage, and strong privacy by design.

Live app:
👉 https://zeromemory-12.streamlit.app/

Why ZeroMemory exists

Most chat applications silently accumulate conversation history. That increases cost, complexity, and privacy risk.

ZeroMemory takes a different approach:

Every request is isolated

No chat history is stored or reused

No user data is persisted

Token usage remains flat and predictable

This makes the app suitable for public demos, cost-sensitive deployments, and privacy-aware use cases.

Key features

Stateless chat (no memory, no context carryover)

Predictable token consumption per request

Clean chat-style UI

Secure API key handling via environment variables

Deployed on Streamlit Cloud

Simple, readable codebase focused on clarity

Tech stack

Python

Streamlit (UI and deployment)

Groq Python SDK (LLM API client)

dotenv (local secret management)

Environment-based configuration (no hardcoded secrets)

How it works (high level)

User submits a message through the chat interface

The message is sent as a single-turn request to the model

The model returns a response

The response is displayed immediately

No conversation state is saved or reused

Each interaction is fully independent.

Project structure
.
├── app.py
├── requirements.txt
├── .gitignore


Secrets are handled via:

.env file for local development

Streamlit Cloud Secrets for production

Design decisions

Stateless architecture
Prevents hidden context growth, reduces cost, and avoids unintended behavior.

No database or session storage
Keeps the app simple, secure, and easy to deploy.

Explicit token limits
Protects against runaway responses and unpredictable billing.

Environment variables for secrets
Ensures API keys are never exposed in source code.

What this project demonstrates

This project showcases practical skills in:

API integration with large language models

Secure secret management

Cost-aware AI application design

Streamlit-based deployment

Writing production-ready, readable Python code

Understanding tradeoffs between stateful vs stateless systems

This is not a toy demo — it reflects real engineering decisions used in production systems.

Future improvements

Optional system prompt configuration

Streaming responses

Rate limiting

Usage analytics

Multi-model support

Author

Built by a student developer focused on applied AI engineering and web deployment, with attention to cost control, security, and clean architecture.
