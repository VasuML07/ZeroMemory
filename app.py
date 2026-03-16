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
    max-width:900px;
    padding-top:3rem;
}

h1{
    font-weight:600;
}

textarea{
    border-radius:10px !important;
    font-size:16px !important;
}

button{
    border-radius:10px !important;
}

.response-box{
    font-size:16px;
    line-height:1.7;
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
# Advanced Controls
# -------------------------
with st.expander("⚙ Advanced settings"):

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
if "prompt" not in st.session_state:
    st.session_state.prompt=""

prompt = st.text_area(
"Prompt",
value=st.session_state.prompt,
placeholder="Describe what you want the AI to generate...",
height=150
)

generate = st.button("Generate", use_container_width=True)

# -------------------------
# Streaming Generator
# -------------------------
def stream_response(user_prompt):

    start = time.time()

    system_prompt = mode_prompts.get(mode,"")

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

    full_text=""
    placeholder=st.empty()

    for chunk in stream:

        delta = chunk.choices[0].delta.content

        if delta:
            full_text += delta
            placeholder.markdown(full_text + "▌")

    placeholder.markdown(full_text)

    latency = round(time.time()-start,2)

    return full_text,latency

# -------------------------
# Run Generation
# -------------------------
if generate and prompt:

    try:

        response_text, latency = stream_response(prompt)

        st.session_state.last_response = response_text

        st.divider()

        token_estimate = int(len(response_text.split()) * 1.3)

        st.caption(
            f"{MODEL_NAME} • {latency}s • ~{token_estimate} tokens"
        )

        # -------------------------
        # Response Tools
        # -------------------------
        col1,col2,col3,col4,col5,col6 = st.columns(6)

        with col1:
            st.download_button(
                "Download",
                response_text,
                file_name="response.txt",
                use_container_width=True
            )

        with col2:
            st.code(response_text)

        with col3:
            if st.button("Summarize",use_container_width=True):
                st.session_state.prompt = f"Summarize this:\n\n{response_text}"
                st.rerun()

        with col4:
            if st.button("Expand",use_container_width=True):
                st.session_state.prompt = f"Expand this explanation:\n\n{response_text}"
                st.rerun()

        with col5:
            if st.button("Simplify",use_container_width=True):
                st.session_state.prompt = f"Explain this more simply:\n\n{response_text}"
                st.rerun()

        with col6:
            if st.button("Improve",use_container_width=True):
                st.session_state.prompt = f"Improve this answer:\n\n{response_text}"
                st.rerun()

        # -------------------------
        # Code detection
        # -------------------------
        if "```" in response_text:
            st.markdown(response_text)
        else:
            st.write(response_text)

        # Expandable view
        with st.expander("Full response"):
            st.markdown(response_text)

    except Exception as e:

        st.error("Request failed.")
        st.code(str(e))
