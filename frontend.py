import streamlit as st
from backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import time
import uuid



# ************************* Utilities Funtions *************************

# generate thread id
def gen_thread_id():
    return str(uuid.uuid4())

# generate previous chat using thread id
def gen_prechat(config):
    state = chatbot.get_state(config)
    messages = state.values.get('messages', [])

    for message in messages:
        if isinstance(message, HumanMessage):
                with st.chat_message('user'):
                    st.write(message.content)

        if isinstance(message, AIMessage):  
                  with st.chat_message('assistant'):
                    st.write(message.content)

# generate new chat with thread id
def new_chat():
    st.session_state.thread_id = None


# initialize variables to track records of chats
if "chat_threads" not in st.session_state:
    st.session_state.chat_threads = retrieve_all_threads()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None


if st.session_state.thread_id is not None:
    CONFIG = {'configurable': {'thread_id': st.session_state.thread_id}}
    gen_prechat(CONFIG)

       

user_input = st.chat_input('Type here...')


# if user enters then, display it
if user_input:
    if st.session_state.thread_id is None:
        st.session_state.thread_id = gen_thread_id()

    CONFIG = {'configurable': {'thread_id': st.session_state.thread_id}}

    if st.session_state.thread_id not in st.session_state.chat_threads:
        st.session_state.chat_threads.append(st.session_state.thread_id)

    with st.chat_message('user'):
        st.write(user_input)


    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        full_response = ""

        for chunk, metadata in chatbot.stream(
            {
                "messages": [HumanMessage(content=user_input)]
            },
            config=CONFIG,
            stream_mode="messages"
        ):
            full_response += chunk.content
            response_placeholder.markdown(full_response)
            time.sleep(0.03)




# ----------------------- SideBar -----------------------
st.sidebar.title('Groq-Chatbot')
if st.sidebar.button('New Chat'):
     new_chat()
     st.rerun()
st.sidebar.header('My Conversations')
for thread_id in st.session_state.chat_threads[::-1]:
     if st.sidebar.button(thread_id):
          st.session_state.thread_id = thread_id
          st.rerun()