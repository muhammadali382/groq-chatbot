from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] 

# ******************* Utitilies Functions *******************

def chat_mode(state: ChatState):
    messages = state['messages']

    response = llm.invoke(messages)

    return {'messages': [response]}

CONFIG = {'configurable': {'thread_id': '1'}}

checkpointer = InMemorySaver()
graph = StateGraph(ChatState)
graph.add_node('chat_mode', chat_mode)
graph.add_edge(START, 'chat_mode')
graph.add_edge('chat_mode', END)
chatbot = graph.compile(checkpointer=checkpointer)


