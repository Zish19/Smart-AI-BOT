import streamlit as st
from agent import chat, read_pdf
import uuid

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Agentic AI",
    page_icon="✨",
    layout="wide",
)

# ===============================
# SESSION STATE INIT
# ===============================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.chats[new_id] = []

# ===============================
# THEME STYLES
# ===============================
if st.session_state.theme == "dark":
    bg = "#0f172a"
    panel = "#020617"
    text = "#e5e7eb"
    bubble_user = "#1f2937"
    bubble_ai = "#020617"
else:
    bg = "#f9fafb"
    panel = "#ffffff"
    text = "#111827"
    bubble_user = "#111827"
    bubble_ai = "#ffffff"

st.markdown(f"""
<style>
body {{ background-color: {bg}; }}
.main {{ background-color: {bg}; color: {text}; }}
.chat-container {{ max-width: 820px; margin: auto; padding-top: 40px; }}
.user {{ background:{bubble_user}; color:white; padding:12px 16px;
border-radius:14px; max-width:75%; margin-left:auto; margin-bottom:12px; }}
.ai {{ background:{bubble_ai}; color:{text}; padding:12px 16px;
border-radius:14px; max-width:75%; margin-bottom:12px;
border:1px solid #e5e7eb; }}
[data-testid="stSidebar"] {{ background-color:{panel}; }}
</style>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR
# ===============================
st.sidebar.markdown("## 🧠 Agentic AI")

# Theme toggle
if st.sidebar.toggle("🌙 Dark mode", st.session_state.theme == "dark"):
    st.session_state.theme = "dark"
else:
    st.session_state.theme = "light"

st.sidebar.divider()

# New chat
if st.sidebar.button("➕ New chat"):
    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.chats[new_id] = []
    st.rerun()

# Chat history
st.sidebar.markdown("### 💬 Chat history")
for cid in st.session_state.chats:
    if st.sidebar.button(f"Chat {cid[:8]}", key=cid):
        st.session_state.current_chat_id = cid
        st.rerun()

st.sidebar.divider()

# File upload
st.sidebar.markdown("### 📎 Upload document")
uploaded_file = st.sidebar.file_uploader(
    "PDF or TXT", type=["pdf", "txt"]
)

document_text = None
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        document_text = read_pdf(uploaded_file)
        st.sidebar.success("Document loaded")
    else:
        document_text = uploaded_file.read().decode("utf-8")
        st.sidebar.success("Document loaded")

# ===============================
# MAIN CHAT UI
# ===============================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

messages = st.session_state.chats[st.session_state.current_chat_id]

if len(messages) == 0:
    st.markdown("### Welcome 👋  \nAsk anything or upload a document.")

for msg in messages:
    role = msg["role"]
    content = msg["content"]
    cls = "user" if role == "user" else "ai"
    st.markdown(f'<div class="{cls}">{content}</div>', unsafe_allow_html=True)

prompt = st.chat_input("Ask anything...")

if prompt:
    messages.append({"role": "user", "content": prompt})
    response = chat(prompt, document_text)
    messages.append({"role": "assistant", "content": response})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

