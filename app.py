import streamlit as st
from agent import chat, read_pdf

st.set_page_config(page_title="Agentic AI Chat", page_icon="🤖")

st.title("🤖 Agentic AI Chat")
st.caption("Ask anything • Upload files • Get smart answers")

# ===============================
# SIDEBAR — FILE UPLOAD
# ===============================
st.sidebar.header("📂 Upload a document")

uploaded_file = st.sidebar.file_uploader(
    "Supported: PDF, TXT",
    type=["pdf", "txt"]
)

document_text = None

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        document_text = read_pdf(uploaded_file)
        st.sidebar.success("PDF loaded successfully")
    else:
        document_text = uploaded_file.read().decode("utf-8")
        st.sidebar.success("Text file loaded successfully")

# ===============================
# CHAT MEMORY
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chat(prompt, document_text)
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
