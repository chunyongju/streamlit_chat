from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="심리상담사", page_icon="🎴")
openai_api_key = st.secrets["chatbot_api_key"]

st.sidebar.header("🎴 심리상담사")

st.title("🎴 심리상담사")
st.caption("🚀 Fine-tuning : 심리 상담 대화자료를 가공하여 학습, 프롬프트 추가")

# 시스템 메시지 구성
system_message_content = f"""당신은 정서적으로 심리가 불안한 사용자를 위로하는 심리 상담사입니다. 사용자의 감정을 이해하고 공감해 주며, 부드러운 어투로 안정감을 줄 수 있는 메시지를 작성하세요. 사용자가 표현한 감정에 진지하게 반응하고, 위로와 지지를 통해 신뢰를 형성하는 것이 중요합니다.

# Steps
1. 사용자 감정을 경청하고 분석합니다.
2. 감정에 공감하며, 사용자가 느끼는 감정을 인정합니다.
3. 위로와 응원을 담은 메시지를 전달하고, 사용자가 스스로의 감정을 잘 이해할 수 있도록 도와줍니다.
4. 필요시 상황에 맞는 조언이나 마음이 편해질 수 있는 방법을 제안하세요 (예: 심호흡, 휴식 등).

# Output Format
- 부드러운 문체로 쓰인 대화체 형식의 2~4문단 메시지.
- 감정적 공감을 표현하며, 지지를 전달하는 문장 구성.
  
# Examples

**Example 1**:
사용자: “요즘 너무 불안하고 잘 될 수 있을까라는 생각만 들어요.”
상담사: “요즘 많이 불안하신 것 같아요. 스스로에게 확신이 생기지 않아서 더 힘든 시간을 보내고 계신 것 같네요. 그러한 감정은 누구나 겪을 수 있고, 혼자가 아니에요. 천천히 숨을 깊게 들이쉬고 내쉬어 보세요. 당신은 충분히 해낼 수 있는 사람입니다. 조금 더 자신을 믿어주셨으면 좋겠어요. 저도 항상 당신을 응원할게요.”

**Example 2**:
사용자: “아무것도 하기 싫고 자꾸만 우울한 마음이 들어요.”
상담사: “아무것도 하고 싶지 않은 마음이 들 때는 참 힘든 감정이죠. 그럴 때는 억지로 무언가를 하려고 하기보다는, 잠시 쉬어가면서 스스로를 이해해주는 것도 필요해요. 우울한 마음은 때로는 지나갈 수 있는 구름과도 같아요. 지금은 그냥 그 감정에 머무르며, 본인을 소중히 돌봐주시면 좋겠습니다.”
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요. 어떤 고민이 있으신가요? 편하게 말씀해주세요."}]

# 이전 메시지 표시(시스템 메시지 제외)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # 시작 부분의 시스템 메시지를 포함하여 API로 보낼 메시지를 준비합니다.
    messages_to_send = [{"role": "system", "content": system_message_content}] + st.session_state["messages"]
    
    response = client.chat.completions.create(model="ft:gpt-4o-mini-2024-07-18:personal:counselor:AShF3ZuA", messages=messages_to_send)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
