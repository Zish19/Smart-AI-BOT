import os
from typing import Optional

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from pypdf import PdfReader

# ===============================
# ENV CHECK
# ===============================
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY missing")

if not os.getenv("TAVILY_API_KEY"):
    raise RuntimeError("TAVILY_API_KEY missing")

# ===============================
# LLM
# ===============================
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.6,
    max_tokens=1200,
)

tavily = TavilySearchResults(max_results=3)

# ===============================
# FILE READING
# ===============================
def read_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# ===============================
# INTELLIGENT CHAT
# ===============================
def chat(user_input: str, document_text: Optional[str] = None) -> str:
    """
    Priority:
    1. Document (if uploaded)
    2. Web search (if needed)
    3. LLM knowledge
    """

    # ---- Document-aware answering ----
    if document_text:
        prompt = f"""
You are an intelligent AI assistant.
Answer the user's question ONLY using the document below.
If the answer is not present, say:
"❌ Not found in the uploaded document."

DOCUMENT:
{document_text[:7000]}

QUESTION:
{user_input}
"""
        return llm.invoke(prompt).content

    # ---- Decide if web search is needed ----
    search_decision_prompt = f"""
Decide whether the following question needs real-time or recent web information.

Question:
{user_input}

Answer ONLY with YES or NO.
"""
    decision = llm.invoke(search_decision_prompt).content.strip().upper()

    if "YES" in decision:
        results = tavily.invoke({"query": user_input})
        if results:
            return results[0]["content"]
        return "No relevant web results found."

    # ---- Default LLM knowledge ----
    return llm.invoke(user_input).content
