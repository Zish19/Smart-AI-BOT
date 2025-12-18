import streamlit as st
from agent import chat, read_pdf
import uuid

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="ZISH",
    page_icon="✨",
    layout="wide",
)

# ===============================
# SESSION STATE
# ===============================
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.current_chat_id = cid
    st.session_state.chats[cid] = []

# ===============================
# TAILWIND CDN + GLOBAL DARK MODE
# ===============================
st.markdown("""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  darkMode: 'class'
}
</script>
</head>
</html>

<style>
/* lock sidebar scroll */
[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    overflow-y: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR (ZISH)
# ===============================
with st.sidebar:
    st.markdown("""
    <div class="h-screen bg-slate-950 text-slate-200 px-4 py-6">
        <h1 class="text-xl font-semibold tracking-wide">ZISH</h1>
        <p class="text-xs text-slate-400 mt-1">AI workspace</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("➕ New chat", use_container_width=True):
        cid = str(uuid.uuid4())
        st.session_state.current_chat_id = cid
        st.session_state.chats[cid] = []
        st.rerun()

    st.markdown("### 💬 History")
    for cid in st.session_state.chats:
        if st.button(f"Chat {cid[:8]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.current_chat_id = cid
            st.rerun()

    st.divider()

    st.markdown("### 📎 Upload")
    uploaded_file = st.file_uploader(
        "PDF or TXT",
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )

document_text = None
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        document_text = read_pdf(uploaded_file)
    else:
        document_text = uploaded_file.read().decode("utf-8")

# ===============================
# MAIN CHAT UI
# ===============================
st.markdown("""
<div class="dark bg-slate-900 min-h-screen">
  <div class="max-w-3xl mx-auto pt-10 px-4">
""", unsafe_allow_html=True)

messages = st.session_state.chats[st.session_state.current_chat_id]

if len(messages) == 0:
    st.markdown("""
    <div class="text-center mb-10">
        <h2 class="text-2xl font-semibold text-slate-100">Welcome to ZISH</h2>
        <p class="text-slate-400 mt-2">Ask anything or upload a document</p>
    </div>
    """, unsafe_allow_html=True)

for msg in messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="flex justify-end mb-3">
            <div class="bg-slate-700 text-white px-4 py-3 rounded-2xl max-w-[75%]">
                {msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="flex justify-start mb-3">
            <div class="bg-slate-800 text-slate-200 px-4 py-3 rounded-2xl max-w-[75%] border border-slate-700">
                {msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

prompt = st.chat_input("Ask anything...")

if prompt:
    messages.append({"role": "user", "content": prompt})
    response = chat(prompt, document_text)
    messages.append({"role": "assistant", "content": response})
    st.rerun()

st.markdown("""
  </div>
</div>
""", unsafe_allow_html=True)

