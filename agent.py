import os
from typing import Optional
from pypdf import PdfReader

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

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
# FILE READER
# ===============================
def read_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ===============================
# CHAT LOGIC
# ===============================
def chat(user_input: str, document_text: Optional[str] = None) -> str:

    # 1️⃣ Document-aware mode
    if document_text:
        prompt = f"""
You are an intelligent AI assistant.
Answer ONLY using the document below.
If the answer is not present, say:
"❌ Not found in the uploaded document."

DOCUMENT:
{document_text[:7000]}

QUESTION:
{user_input}
"""
        return llm.invoke(prompt).content

    # 2️⃣ Decide if web search is needed
    decision_prompt = f"""
Does this question require recent or real-time information?

Question: {user_input}

Answer only YES or NO.
"""
    decision = llm.invoke(decision_prompt).content.strip().upper()

    if "YES" in decision:
        results = tavily.invoke({"query": user_input})
        if results:
            return results[0]["content"]
        return "No relevant web results found."

    # 3️⃣ Default LLM knowledge
    return llm.invoke(user_input).content
