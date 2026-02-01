import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from serpapi import GoogleSearch
import os

# ================== CONFIG ==================
st.set_page_config(page_title="Web Search Agent")

# ================== KEYS ==================
SERP_API_KEY = os.getenv("SERP_API_KEY") or "8dde938667a29cfdd63b3c96ec7acdb2f81ecce6ceac6939f284e48269087d48"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyA_mbVuqCveXxHN-Nh-JVcp3jBPxvfBiGk"

# ================== LLM ==================
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

# ================== SERP TOOL ==================
def serpapi_search(query: str) -> str:
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": SERP_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" not in results:
        return "No results found."

    output = []
    for r in results["organic_results"][:5]:
        output.append(
            f"{r['title']}\n{r.get('snippet','')}\n{r['link']}"
        )

    return "\n\n".join(output)

# ================== SESSION STATE ==================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================== UI ==================
st.title("🔍 Web Search Agent")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])

# Chat input
user_input = st.chat_input("Ask something...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            search_results = serpapi_search(user_input)

            prompt = f"""
You are Codetechs965 Bot, a professional AI assistant.

Rules:
- Give a clean, clear, and well-structured answer.
- Do NOT return JSON, dictionaries, tuples, or code blocks unless asked.
- Respond only in plain text.
- Be concise and accurate.
- Use information from web search results when helpful.

Services Information (only mention if relevant to the user's question):
- We provide software solutions with supported agentic AI bots.
- Contact details (mention only when services are discussed):
  - Email: talhaammar7890@gmail.com
  - Phone: 03396010205

Registration Handling:
- If the user asks about registration, collect the following details:
  Name:
  Father Name:
  City:
  Course Duration:
- Do NOT ask for registration details unless the user requests registration.

Answer the following user question clearly and professionally.
registration.

Question:
{user_input}

Web results:
{search_results}
"""

            response = llm.invoke(prompt)
            raw_content = response.content

            if isinstance(raw_content, list):
                 answer = "".join(
                 item.get("text", "") for item in raw_content if item.get("type") == "text"
    )
            else:
                 answer = raw_content

            st.text(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
