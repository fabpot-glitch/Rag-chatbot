import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="centered"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Title styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #8b8fa8;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Chat bubbles */
    .stChatMessage {
        border-radius: 12px;
        padding: 4px 8px;
    }

    /* Input box */
    .stChatInputContainer {
        border-top: 1px solid #2a2d3e;
        padding-top: 12px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #13151f;
        border-right: 1px solid #1e2030;
    }

    /* Status badge */
    .status-badge {
        display: inline-block;
        background-color: #1a2e1a;
        color: #4ade80;
        border: 1px solid #4ade80;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 16px;
    }

    /* Sidebar section headers */
    .sidebar-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #5a5f7a;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── API URL ──────────────────────────────────────────────────────────────────
API_URL = "http://127.0.0.1:8000"
# After deploying to Render, comment above and uncomment below:
# API_URL = "https://your-app-name.onrender.com"

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🧠 DocuMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Intelligent document assistant — ask anything about your PDF</div>', unsafe_allow_html=True)
st.markdown('<span class="status-badge">● Online</span>', unsafe_allow_html=True)
st.divider()

# ─── Session State ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── Welcome message (shown only once) ───────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "👋 Hello! I'm your document assistant. "
            "I've analysed your PDF and I'm ready to answer your questions. "
            "What would you like to know?"
        )

# ─── Render chat history ─────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        st.caption(msg.get("time", ""))

# ─── Chat input ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about your document..."):

    now = datetime.now().strftime("%I:%M %p")

    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(now)
    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})

    with st.chat_message("assistant"):
        with st.spinner("Analysing document..."):
            try:
                resp = requests.get(
                    f"{API_URL}/ask",
                    params={"question": prompt},
                    timeout=30
                )
                resp.raise_for_status()
                answer = resp.json()["answer"]

            except requests.exceptions.ConnectionError:
                answer = (
                    "⚠️ Unable to reach the backend server.\n\n"
                    "Please ensure the API is running:\n\n"
                    "```\nuvicorn app.main:app --reload\n```"
                )
            except requests.exceptions.Timeout:
                answer = "⚠️ The request timed out. The server may be starting up — please try again."
            except Exception as e:
                answer = f"⚠️ An unexpected error occurred: `{str(e)}`"

        st.markdown(answer)
        st.caption(now)
        st.session_state.messages.append({"role": "assistant", "content": answer, "time": now})

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 DocuMind AI")
    st.markdown("Your intelligent document assistant, powered by retrieval-augmented generation.")
    st.divider()

    st.markdown('<div class="sidebar-label">Document</div>', unsafe_allow_html=True)
    st.info("📄 sample.pdf — loaded and indexed")

    st.divider()

    st.markdown('<div class="sidebar-label">Session</div>', unsafe_allow_html=True)
    msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.metric("Questions Asked", msg_count)

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("© 2026 DocuMind AI. All rights reserved.")


    