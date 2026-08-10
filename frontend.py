import streamlit as st
from backend import chatbot, CONFIG
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import time
import uuid



# ************************* Utilities Funtions *************************

# generate thread id
def gen_thread_id():
    return str(uuid.uuid4())

# generate previous chat using thread id
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

# generate new chat with thread id
def new_chat():
    thread_id = gen_thread_id()
    st.session_state.chat_threads.append(thread_id)
    st.session_state.thread_id = thread_id


# initialize variables to track records of chats
if "chat_threads" not in st.session_state:
    st.session_state.chat_threads = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = gen_thread_id()
    st.session_state.chat_threads.append(
        st.session_state.thread_id
    )

# Get Current thread id for the chat
CONFIG = {'configurable': {'thread_id': st.session_state.thread_id}}

# generate previous chat of this thread id if available
gen_prechat()        

user_input = st.chat_input('Type here...')


# if user enters then, display it
if user_input:
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
for thread_id in st.session_state.chat_threads:
     if st.sidebar.button(thread_id):
          st.session_state.thread_id = thread_id
          st.rerun()