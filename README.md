ZeroMemory — Stateless AI Chat Application

ZeroMemory is a stateless AI-powered chat application built with Streamlit, designed to deliver fast, predictable, and privacy-conscious interactions.
Each user query is handled independently, with no conversation memory, ensuring consistent token usage, minimal cost overhead, and zero data retention.

Live Application:
https://zeromemory-12.streamlit.app/

Table of Contents

Overview

Problem Statement

Solution Approach

Key Features

Architecture & Design Decisions

Tech Stack

Project Structure

Setup & Deployment

Security & Privacy

Limitations

Future Enhancements

What This Project Demonstrates

Overview

Most conversational AI applications retain chat history across turns. While useful, this approach increases token usage, operational cost, and privacy risk.

ZeroMemory intentionally avoids that pattern.

This application follows a single-turn, stateless request model, where each prompt is processed in isolation. The result is a clean, cost-controlled, and privacy-first chat system suitable for public deployment.

Problem Statement

Traditional chat applications often suffer from:

Unbounded token growth due to accumulating context

Increasing operational costs over time

Implicit storage of user conversations

Complex session and state management

These issues become critical when deploying public or cost-sensitive AI applications.

Solution Approach

ZeroMemory addresses these challenges by adopting a stateless architecture:

Each user message is sent as a standalone request

No chat history is stored or reused

No database or session storage is required

Token usage remains constant per interaction

This approach prioritizes predictability, simplicity, and privacy.

Key Features

Stateless chat design (no memory, no session state)

Predictable token consumption per request

Clean chat-style user interface

Secure API key handling via environment variables

Explicit output length limits for cost control

Cloud deployment using Streamlit

Architecture & Design Decisions
Stateless Interaction Model

Each request includes only the current user message.
No previous context is sent to the model.

Benefits:

Flat token usage

Lower operational cost

No context leakage

Simplified debugging

Explicit Token Control

A hard cap on response length prevents runaway generations and unexpected billing.

Environment-Based Secret Management

API keys are never hard-coded and are injected at runtime via environment variables or platform secrets.

Minimal Dependency Footprint

Only essential libraries are used to reduce complexity and improve reliability.

Tech Stack

Python

Streamlit — UI and hosting

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

Clone the repository

Create a .env file with:

GROQ_API_KEY=your_api_key_here


Install dependencies:

pip install -r requirements.txt


Run the app:

python -m streamlit run app.py

Deployment (Streamlit Cloud)

Push app.py and requirements.txt to GitHub

Add GROQ_API_KEY in Streamlit Cloud → App Settings → Secrets

Deploy using app.py as the entry point

No .env file is used in production.

Security & Privacy

No user input is stored

No conversation history is retained

API keys are never exposed in source code

Secrets are managed via environment variables

Stateless design minimizes data risk

Limitations

No multi-turn conversation memory

No personalization across messages

No persistent user sessions

These limitations are intentional tradeoffs to ensure cost and privacy guarantees.

Future Enhancements

Optional system prompt configuration

Streaming responses

Rate limiting and abuse protection

Usage analytics dashboard

Model selection controls

What This Project Demonstrates

This project reflects real-world engineering considerations, including:

Applied AI integration (LLM APIs)

Cost-aware system design

Stateless architecture patterns

Secure secret management

Cloud deployment workflows

Writing maintainable, production-ready Python code
