from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="천부장bot", page_icon="💬")
openai_api_key = st.secrets["chatbot_api_key"]

# with st.sidebar:
#    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.sidebar.header("💬 천부장bot")

st.title("💬 천부장bot")
st.caption("🚀 Fine-tuning : 천부장의 카톡, 네이트온 대화를 DATA SET으로 학습")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
#    if not openai_api_key:
#        st.info("Please add your OpenAI API key to continue.")
#        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="ft:gpt-4o-2024-08-06:personal:chunbot:AHpPj9PJ", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    completion = response.usage.completion_tokens
    prompt = response.usage.prompt_tokens
    total = response.usage.total_tokens
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(f"{msg} (입력: {completion}, 응답: {prompt}, 총: {total})")
