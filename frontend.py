import streamlit as st
from backend import chatbot, CONFIG
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ************************* Utilities Funtions *************************

def gen_prechat():
    state = chatbot.get_state(CONFIG)
    messages = state.values.get('messages', [])

    for message in messages:
        if isinstance(message, HumanMessage):
                with st.chat_message('user'):
                    st.write(message.content)

        if isinstance(message, AIMessage):  
                  with st.chat_message('assistant'):
                    st.write(message.content)


gen_prechat()        
      
user_input = st.chat_input('Type here...')



if user_input:
    with st.chat_message('user'):
        st.write(user_input)

    response = chatbot.invoke(
        {
              'messages': [HumanMessage(content=user_input)]
        }, 
        config=CONFIG
        )

    ai_message = response['messages'][-1].content
    with st.chat_message('assistant'):
        st.write(ai_message)
        