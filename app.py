import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

# Get API key (Streamlit Cloud or local .env)
api_key = None

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found. Add it to Streamlit secrets or .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

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
# Sidebar controls
# -------------------------
st.sidebar.header("Settings")

model_name = st.sidebar.selectbox(
    "Model",
    [
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]
)

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
@st.cache_resource
def load_model(name):
    return genai.GenerativeModel(name)


def get_response(user_message):

    start_time = time.time()

    model = load_model(model_name)

    response = model.generate_content(
        user_message,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens
        }
    )

    latency = round(time.time() - start_time, 2)

    text = ""

    try:
        text = response.text
    except Exception:
        text = "No response returned."

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
                    f"Model: {model_name} | Latency: {latency}s | Max Tokens: {max_tokens}"
                )

            except Exception as e:

                st.error("Request failed.")
                st.code(str(e))
