import os

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

st.set_page_config(
    page_title="YashX AI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #17211d;
        --muted: #78837d;
        --green: #176b52;
        --green-light: #eaf4ef;
        --line: #e9eeea;
        --surface: #ffffff;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 50% -18%, rgba(207, 231, 215, .48), transparent 38%),
            #fbfcfb;
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: #f5f8f5;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: .7rem;
        margin-bottom: 2rem;
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: -.04em;
    }

    .brand-mark {
        display: grid;
        width: 2rem;
        height: 2rem;
        place-items: center;
        border-radius: .7rem;
        background: var(--green);
        color: white;
        font-size: 1rem;
    }

    .sidebar-label {
        margin: 1.6rem 0 .55rem;
        color: var(--muted);
        font-size: .7rem;
        font-weight: 700;
        letter-spacing: .1em;
        text-transform: uppercase;
    }

    .model-badge {
        padding: .75rem .85rem;
        border: 1px solid var(--line);
        border-radius: .8rem;
        background: var(--surface);
        color: #46544c;
        font-size: .83rem;
    }

    .model-dot {
        display: inline-block;
        width: .48rem;
        height: .48rem;
        margin-right: .45rem;
        border-radius: 50%;
        background: #43a779;
        vertical-align: .06rem;
    }

    .hero {
        padding: 4.2rem 0 2rem;
        text-align: center;
    }

    .hero-mark {
        display: inline-grid;
        width: 3.2rem;
        height: 3.2rem;
        margin-bottom: 1.2rem;
        place-items: center;
        border: 1px solid #dbe9df;
        border-radius: 1.1rem;
        background: linear-gradient(145deg, #f2f8f3, #e4f1e8);
        color: var(--green);
        font-size: 1.4rem;
    }

    .hero h1 {
        margin: 0;
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 6vw, 2.65rem);
        font-weight: 800;
        letter-spacing: -.065em;
    }

    .hero p {
        margin: .75rem 0 0;
        color: var(--muted);
        font-size: 1rem;
    }

    .suggestion-label {
        margin: 1.3rem 0 .65rem;
        color: var(--muted);
        font-size: .76rem;
        font-weight: 600;
        text-align: center;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 1rem;
        background: var(--surface);
    }

    [data-testid="stChatInput"] {
        border-color: #dfe7e1;
        border-radius: 1rem;
        background: var(--surface);
    }

    .stButton > button {
        min-height: 2.8rem;
        border: 1px solid var(--line);
        border-radius: .8rem;
        background: var(--surface);
        color: #3b4941;
        font-size: .83rem;
        transition: border-color .15s ease, background .15s ease, transform .15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #a9cbb6;
        background: #f4f9f5;
        color: var(--green);
    }

    .footnote {
        margin-top: 1.3rem;
        color: #929c96;
        font-size: .74rem;
        text-align: center;
    }

    @media (max-width: 640px) {
        .hero {
            padding-top: 2.5rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []


def select_prompt(prompt: str) -> None:
    st.session_state.pending_prompt = prompt


with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">✦</span>YashX AI</div>',
        unsafe_allow_html=True,
    )

    if st.button("＋  New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="sidebar-label">Your assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="model-badge"><span class="model-dot"></span>Gemini 2.5 Flash</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="footnote">Helpful answers, powered by Gemini.</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="hero">
        <div class="hero-mark">✦</div>
        <h1>What can I help with?</h1>
        <p>Ask a question, explore an idea, or get something done.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown('<div class="suggestion-label">TRY ASKING</div>', unsafe_allow_html=True)
    suggestions = [
        "Explain machine learning simply",
        "Help me plan a study schedule",
        "Give me ideas for a Python project",
        "Summarize the benefits of reading",
    ]
    columns = st.columns(2)
    for index, suggestion in enumerate(suggestions):
        with columns[index % 2]:
            st.button(
                suggestion,
                key=f"suggestion_{index}",
                use_container_width=True,
                on_click=select_prompt,
                args=(suggestion,),
            )
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Message YashX AI…")
if prompt is None:
    prompt = st.session_state.pop("pending_prompt", None)

if prompt:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY to a .env file "
            "in the project folder, then restart the app."
        )
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                chat_model = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    temperature=0.7,
                )
                response = chat_model.invoke(
                    [
                        (message["role"], message["content"])
                        for message in st.session_state.messages
                    ]
                )
                answer = response.content
                if not isinstance(answer, str):
                    answer = "\n".join(
                        block["text"]
                        for block in answer
                        if isinstance(block, dict) and isinstance(block.get("text"), str)
                    )
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown('<div class="footnote">CampusX AI can make mistakes. Check important information.</div>', unsafe_allow_html=True)
