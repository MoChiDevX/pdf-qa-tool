import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import qa_agent

st.title('🌟AI智能PDF解析助手')

with st.sidebar:
    openai_api_key = st.text_input('请输入OpenAI API密钥：', type = 'password')
    st.markdown = ('[获取OpenAI API key](https://platform.openai.com/api-keys)')
    base_url = st.text_input('请输入镜像网站地址(如有)：')

if 'memory' not in st.session_state:
    st.session_state['memory'] = ConversationBufferMemory(
        return_messages = True,
        memory_key = 'chat_history',
        output_key = 'answer'
    )

uploaded_file = st.file_uploader('上传你的PDF文件：', type = 'pdf')
question = st.text_input('提问pdf内容', disabled=not uploaded_file)
submit = st.button('发送问题')

if uploaded_file and question and submit and not openai_api_key:
    st.info('请输入API密钥')


if uploaded_file and question and submit and openai_api_key:
    try:
        if base_url:
            with st.spinner('AI正在思考…'):
                response = qa_agent(openai_api_key, st.session_state['memory'], uploaded_file, question, base_url)
        if not base_url:
            with st.spinner('AI正在思考…'):
                response = qa_agent(openai_api_key, st.session_state['memory'], uploaded_file, question)
    except Exception as e:
        st.error(f"🚨 出现错误：{str(e)}")
        
    st.write('### 答案')
    st.write(response['answer'])
    st.session_state['chat_history'] = response['chat_history']

if 'chat_history' in st.session_state:
    with st.expander('历史消息'):
        for i in range(0,len(st.session_state['chat_history']),2):
            human_message = st.session_state['chat_history'][i]
            ai_message = st.session_state['chat_history'][i+1]
            st.write(human_message.content)
            st.write(ai_message.content)
            if i < len(st.session_state['chat_history']) - 2:
                st.divider()


