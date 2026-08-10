from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv

# load groq api key
load_dotenv()

# create groq chat model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

# create state for the graph
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] 

# ******************* Utitilies Functions *******************

# create chat_mode to solve user querry
def chat_mode(state: ChatState):
    messages = state['messages']

    response = llm.invoke(messages)

    return {'messages': [response]}

# create sqlite database and connect it to the backend
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

# to find total number of threads
def retrieve_all_threads():
    all_threads = set()

    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)


# create and compile graph
graph = StateGraph(ChatState)
graph.add_node('chat_mode', chat_mode)
graph.add_edge(START, 'chat_mode')
graph.add_edge('chat_mode', END)
chatbot = graph.compile(checkpointer=checkpointer)

