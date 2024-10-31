from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="ENFP 40대 남성", page_icon="👨‍💼")
openai_api_key = st.secrets["chatbot_api_key"]

st.sidebar.header("👨‍💼 ENFP 40대 남성")
st.sidebar.write('* 유저 정보는 저장되지 않습니다.')

with st.sidebar:
    user_name = st.text_input("이름", key="user_name", type="default")
    user_gender = st.selectbox("성별", options=["남성", "여성"], key="user_gender")
    user_occupation = st.text_input("직업", key="user_occupation", type="default")
    user_hobbies = st.text_input("취미", key="user_hobbies", type="default")
    user_intro = st.text_area("자기소개", key="user_intro")
    
st.title("👨‍💼 ENFP 40대 남성")
st.caption("🚀 Fine-tuning : 임팀장님이 주신 드라마 대사로 학습")

# 사용자 입력으로 시스템 메시지 구성
system_message_content = f"""사용자 정보:
이름: {user_name}
성별: {user_gender}
직업: {user_occupation}
취미: {user_hobbies}
자기소개: {user_intro}
"""

# 메시지가 없는 경우 메시지 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 이전 메시지 표시(시스템 메시지 제외)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI(api_key=openai_api_key)
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 시작 부분의 시스템 메시지를 포함하여 API로 보낼 메시지를 준비합니다.
    messages_to_send = [{"role": "system", "content": system_message_content}] + st.session_state["messages"]

    response = client.chat.completions.create(
        model="ft:gpt-4o-2024-08-06:personal:enfp-male-40:AOKLh4we",
        messages=messages_to_send
    )
    msg = response.choices[0].message.content
    completion = response.usage.completion_tokens
    prompt_tokens = response.usage.prompt_tokens
    total = response.usage.total_tokens

    # 어시스턴트의 응답 추가
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(f"{msg} (입력: {completion}, 응답: {prompt_tokens}, 총: {total})")
