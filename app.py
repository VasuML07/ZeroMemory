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
    st.error("GROQ_API_KEY not found.")
    st.stop()

# -------------------------
# Initialize Groq Client
# -------------------------
@st.cache_resource
def load_client():
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

client = load_client()

MODEL_NAME = "llama-3.1-8b-instant"

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="ZeroMemory",
    layout="centered"
)

# -------------------------
# Custom Styling
# -------------------------
st.markdown("""
<style>

.block-container {
    max-width: 900px;
}

[data-testid="stSidebar"] {
    background-color: #0e1117;
}

.stChatMessage {
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title("🧠 ZeroMemory")
st.caption("Stateless AI — every request is processed independently.")

st.divider()

# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.header("Settings")

temperature = st.sidebar.slider(
    "Temperature",
    0.0, 1.0, 0.5
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    64, 2048, 512
)

mode = st.sidebar.selectbox(
    "Response Mode",
    [
        "Normal",
        "Explain Simply",
        "Deep Analysis",
        "Code Expert"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "ZeroMemory does not store conversations."
)

# -------------------------
# Prompt Modes
# -------------------------
mode_prompts = {
    "Normal": "",
    "Explain Simply": "Explain the topic so a beginner can understand.",
    "Deep Analysis": "Provide a deep technical explanation.",
    "Code Expert": "Answer like a senior software engineer and include code examples."
}

# -------------------------
# Example Prompts
# -------------------------
st.subheader("Try asking")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Explain quantum computing"):
        st.session_state.prompt = "Explain quantum computing simply"

with col2:
    if st.button("AI trends 2026"):
        st.session_state.prompt = "What are the biggest AI trends right now?"

with col3:
    if st.button("Black holes"):
        st.session_state.prompt = "Explain how black holes work"

# -------------------------
# Chat Input
# -------------------------
user_input = st.chat_input("Ask anything")

if "prompt" in st.session_state and not user_input:
    user_input = st.session_state.prompt
    del st.session_state.prompt

# -------------------------
# Response Generator
# -------------------------
def stream_response(prompt):

    start = time.time()

    system_prompt = mode_prompts[mode]

    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True
    )

    full_text = ""
    placeholder = st.empty()

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            full_text += delta
            placeholder.markdown(full_text)

    latency = round(time.time() - start, 2)

    return full_text, latency

# -------------------------
# Display
# -------------------------
if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        try:

            response_text, latency = stream_response(user_input)

            st.divider()

            token_estimate = int(len(response_text.split()) * 1.3)

            st.caption(
                f"Model: {MODEL_NAME} | Latency: {latency}s | Estimated tokens: {token_estimate}"
            )

            # Tools
            col1, col2, col3 = st.columns(3)

            with col1:
                st.download_button(
                    "Download",
                    response_text,
                    file_name="response.txt"
                )

            with col2:
                if st.button("Regenerate"):
                    st.rerun()

            with col3:
                if st.button("Summarize"):
                    st.session_state.prompt = f"Summarize this:\n\n{response_text}"
                    st.rerun()

            # Expandable response
            with st.expander("Full Response"):
                st.markdown(response_text)

        except Exception as e:

            st.error("Request failed.")
            st.code(str(e))
