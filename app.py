import os
import time
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# -------------------------
# Load environment
# -------------------------
load_dotenv()

api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found.")
    st.stop()

# -------------------------
# Groq Client
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
# Page
# -------------------------
st.set_page_config(
    page_title="ZeroMemory",
    layout="centered"
)

# -------------------------
# Styling
# -------------------------
st.markdown("""
<style>

.block-container{
    max-width:820px;
    padding-top:3rem;
}

h1{
    font-weight:600;
}

textarea{
    border-radius:10px !important;
}

button{
    border-radius:10px !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title("🧠 ZeroMemory")
st.caption("Stateless AI — every request runs independently.")

st.divider()

# -------------------------
# Control Bar
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.slider(
        "Temperature",
        0.0,1.0,0.5
    )

with col2:
    max_tokens = st.slider(
        "Max tokens",
        64,2048,512
    )

with col3:
    mode = st.selectbox(
        "Mode",
        [
            "Normal",
            "Explain Simply",
            "Deep Analysis",
            "Code Expert"
        ]
    )

# -------------------------
# Mode Prompts
# -------------------------
mode_prompts = {
"Normal":"",
"Explain Simply":"Explain clearly so a beginner understands.",
"Deep Analysis":"Provide a deep expert-level explanation.",
"Code Expert":"Answer like a senior software engineer with code examples."
}

# -------------------------
# Prompt
# -------------------------
prompt = st.text_area(
"Prompt",
placeholder="Describe what you want the AI to generate...",
height=140
)

generate = st.button("Generate", use_container_width=True)

# -------------------------
# Response Generator
# -------------------------
def stream_response(user_prompt):

    start = time.time()

    system_prompt = mode_prompts[mode]

    messages = []

    if system_prompt:
        messages.append({
            "role":"system",
            "content":system_prompt
        })

    messages.append({
        "role":"user",
        "content":user_prompt
    })

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

    latency = round(time.time() - start,2)

    return full_text, latency

# -------------------------
# Run Generation
# -------------------------
if generate and prompt:

    try:

        response_text, latency = stream_response(prompt)

        st.divider()

        token_estimate = int(len(response_text.split()) * 1.3)

        st.caption(
            f"Model: {MODEL_NAME} | Latency: {latency}s | Estimated tokens: {token_estimate}"
        )

        # -------------------------
        # Response Tools
        # -------------------------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.download_button(
                "Download",
                response_text,
                file_name="response.txt",
                use_container_width=True
            )

        with col2:
            if st.button("Summarize", use_container_width=True):
                st.rerun()

        with col3:
            if st.button("Expand", use_container_width=True):
                st.rerun()

        with col4:
            if st.button("Simplify", use_container_width=True):
                st.rerun()

        # Expandable response
        with st.expander("Full response"):
            st.markdown(response_text)

    except Exception as e:

        st.error("Request failed.")
        st.code(str(e))
