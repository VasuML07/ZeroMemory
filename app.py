import os
import time
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

api_key = None

if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Add it to Streamlit secrets or .env file.")
    st.stop()

# -------------------------
# Initialize Groq client
# -------------------------
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "llama-3.1-8b-instant"

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="ZeroMemory",
    layout="centered"
)

# -------------------------
# UI Header
# -------------------------
st.title("🧠 ZeroMemory")
st.caption("Stateless AI — every request is processed independently.")

st.divider()

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("Settings")

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.5
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    min_value=64,
    max_value=2048,
    value=512
)

st.sidebar.divider()

st.sidebar.caption(
    "ZeroMemory does not store conversations. Each request is isolated."
)

# -------------------------
# Example prompts
# -------------------------
st.subheader("Try asking")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Explain quantum computing"):
        st.session_state.prompt = "Explain quantum computing simply"

with col2:
    if st.button("Summarize AI trends"):
        st.session_state.prompt = "What are the major AI trends in AI right now?"

with col3:
    if st.button("How do black holes work?"):
        st.session_state.prompt = "Explain how black holes work in simple terms."

# -------------------------
# Chat input
# -------------------------
user_input = st.chat_input("Ask anything")

if "prompt" in st.session_state and not user_input:
    user_input = st.session_state.prompt
    del st.session_state.prompt


# -------------------------
# Response function
# -------------------------
def get_response(user_message):

    start_time = time.time()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": user_message}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    latency = round(time.time() - start_time, 2)

    text = response.choices[0].message.content

    return text, latency


# -------------------------
# Display response
# -------------------------
if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Generating response..."):

            try:

                response, latency = get_response(user_input)

                st.markdown(response)

                st.divider()

                st.caption(
                    f"Model: {MODEL_NAME} | Latency: {latency}s | Max Tokens: {max_tokens}"
                )

            except Exception as e:

                st.error("Request failed.")
                st.code(str(e))
