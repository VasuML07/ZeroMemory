import os
import time
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# -------------------------
# Load env variables
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
# Load Groq Client
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
    layout="wide"
)

# -------------------------
# Styling
# -------------------------
st.markdown("""
<style>

.block-container{
    max-width:1100px;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0e1117,#090c10);
}

.stChatMessage{
    border-radius:16px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title("🧠 ZeroMemory")
st.caption("Stateless AI — each request runs independently.")

st.divider()

# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.header("Settings")

temperature = st.sidebar.slider("Temperature",0.0,1.0,0.5)
max_tokens = st.sidebar.slider("Max Tokens",64,2048,512)

mode = st.sidebar.selectbox(
"Thinking Mode",
[
"Normal",
"Explain Simply",
"Deep Analysis",
"Code Expert",
"Teacher Mode",
"Startup Advisor"
]
)

output_format = st.sidebar.selectbox(
"Output Format",
[
"Normal",
"Bullet Summary",
"Table",
"Step-by-step"
]
)

st.sidebar.divider()

st.sidebar.caption("ZeroMemory stores no conversations.")

# -------------------------
# Mode Prompts
# -------------------------
mode_prompts = {
"Normal":"",
"Explain Simply":"Explain clearly so a beginner understands.",
"Deep Analysis":"Provide a deep expert-level explanation.",
"Code Expert":"Answer like a senior software engineer with code examples.",
"Teacher Mode":"Explain as a teacher guiding a student.",
"Startup Advisor":"Answer like a startup advisor with practical insight."
}

format_prompts = {
"Normal":"",
"Bullet Summary":"Respond using concise bullet points.",
"Table":"Present the answer as a structured table.",
"Step-by-step":"Explain step by step."
}

# -------------------------
# Prompt History
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Prompt Workspace
# -------------------------
prompt = st.text_area(
"Prompt",
placeholder="Describe what you want the AI to generate...",
height=120
)

# -------------------------
# Preset Prompts
# -------------------------
st.subheader("Quick Prompts")

col1,col2,col3,col4 = st.columns(4)

with col1:
    if st.button("Explain quantum computing"):
        prompt="Explain quantum computing simply"

with col2:
    if st.button("AI trends 2026"):
        prompt="What are the biggest AI trends in AI?"

with col3:
    if st.button("Startup idea"):
        prompt="Generate a startup idea using AI"

with col4:
    if st.button("Debug Python"):
        prompt="Help debug this Python code"

# -------------------------
# Run Button
# -------------------------
run = st.button("Generate")

# -------------------------
# Streaming Response
# -------------------------
def stream_response(user_prompt):

    start=time.time()

    system_parts=[
        mode_prompts[mode],
        format_prompts[output_format]
    ]

    system_prompt=" ".join([p for p in system_parts if p])

    messages=[]

    if system_prompt:
        messages.append({"role":"system","content":system_prompt})

    messages.append({"role":"user","content":user_prompt})

    stream=client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True
    )

    full_text=""
    placeholder=st.empty()

    for chunk in stream:

        delta=chunk.choices[0].delta.content

        if delta:
            full_text+=delta
            placeholder.markdown(full_text)

    latency=round(time.time()-start,2)

    return full_text,latency

# -------------------------
# Run Generation
# -------------------------
if run and prompt:

    st.session_state.history.append(prompt)

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        try:

            response_text,latency=stream_response(prompt)

            st.divider()

            token_estimate=int(len(response_text.split())*1.3)

            st.caption(
            f"Model: {MODEL_NAME} | Latency: {latency}s | Estimated tokens: {token_estimate}"
            )

            # -------------------------
            # Response Tools
            # -------------------------
            col1,col2,col3,col4,col5=st.columns(5)

            with col1:
                st.download_button(
                "Download",
                response_text,
                file_name="response.txt"
                )

            with col2:
                if st.button("Copy"):
                    st.code(response_text)

            with col3:
                if st.button("Summarize"):
                    st.session_state.prompt=f"Summarize this:\n\n{response_text}"
                    st.rerun()

            with col4:
                if st.button("Expand"):
                    st.session_state.prompt=f"Expand this explanation:\n\n{response_text}"
                    st.rerun()

            with col5:
                if st.button("Simplify"):
                    st.session_state.prompt=f"Explain this more simply:\n\n{response_text}"
                    st.rerun()

            # Expandable view
            with st.expander("Full Response"):
                st.markdown(response_text)

        except Exception as e:

            st.error("Request failed.")
            st.code(str(e))

# -------------------------
# Prompt History Sidebar
# -------------------------
st.sidebar.subheader("Recent Prompts")

for h in st.session_state.history[-5:][::-1]:
    st.sidebar.write("•",h)
