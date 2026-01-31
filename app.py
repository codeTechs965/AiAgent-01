import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from serpapi import GoogleSearch
import os

# ================== CONFIG ==================
st.set_page_config(page_title="Web Search Agent")

# ================== KEYS ==================
SERP_API_KEY = os.getenv("SERP_API_KEY") or "8dde938667a29cfdd63b3c96ec7acdb2f81ecce6ceac6939f284e48269087d48"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyDDvk-BiY1o8eBnDb2VR0nwGk3uvBV0OMI"

# ================== LLM ==================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
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
please give only content dont add dictionary, tuple . please give an answer your name is Codetechs965 bot and you are going to giving reply.Clean and clear response.Tell user about our services if they ask 
. Our services are we are providing softwares with supported agentic bot .please mention my phone number and email after providing user information of my services. My gmail is talhaammar7890@gmail.com and phonenumber is 03396010205.Please fill also his name if he/she asked for registration . Form informstion Name:    ,Father Name:     ,City:     , Course Duration    . and other information only if he required information then you should asked for form registration.

Question:
{user_input}

Web results:
{search_results}
"""

            response = llm.invoke(prompt)
            answer = response.content

            st.text(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
