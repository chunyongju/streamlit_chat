from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="심리상담사", page_icon="🎴")
openai_api_key = st.secrets["chatbot_api_key"]

st.sidebar.header("🎴 심리상담사")

st.title("🎴 심리상담사")
st.caption("🚀 Fine-tuning : 심리 상담 대화자료를 가공하여 학습")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요. 어떤 고민이 있으신가요? 편하게 말씀해주세요."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="ft:gpt-4o-mini-2024-07-18:personal:counselor:AShF3ZuA", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
