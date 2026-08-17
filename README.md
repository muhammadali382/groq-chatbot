# Groq Chatbot

A lightweight conversational chatbot built with Streamlit, LangGraph, and Groq's LLM API. The app lets you start a chat, continue thread-based conversations, and persist conversation state in SQLite so previous chats can be revisited.

## What this project does

- Uses `ChatGroq` to generate responses with the `llama-3.3-70b-versatile` model
- Builds a LangGraph workflow with a simple stateful chat node
- Stores checkpoints in SQLite so each conversation can be resumed by thread ID
- Exposes a Streamlit frontend for interactive chat and thread history
- Supports a "New Chat" flow and a sidebar with saved conversation IDs

## Project structure

- `backend.py` — LangGraph chatbot graph, model setup, and SQLite checkpoint configuration
- `frontend.py` — Streamlit UI for sending prompts and viewing conversation history
- `chatbot.db` — SQLite database used by LangGraph for conversation state persistence
- `pyproject.toml` — Python project metadata and dependencies
- `.env` — environment file for local API configuration

## Tech stack

- Python
- Streamlit
- LangChain
- LangGraph
- LangGraph SQLite checkpointing
- Groq API
- SQLite

## Requirements

- Python 3.14+ (as declared in the project metadata)
- A Groq API key
- Access to the internet for Groq inference

## Setup

1. Clone the repository and move into the project folder.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   pip install -U pip
   pip install "langchain>=1.3.14" "langchain-core>=1.5.3" "langchain-groq>=1.1.3" "langgraph>=1.2.10" "langgraph-checkpoint-sqlite>=3.1.1" "python-dotenv>=1.2.2" "streamlit>=1.61.1"
   ```

   If you use `uv`, this repo also includes a lock file and the project is compatible with `uv sync`.

## Environment configuration

Create a `.env` file in the project root with your Groq key:

```env
GROQ_API_KEY=your_api_key_here
```

The app loads this file with `python-dotenv` before creating the Groq client.

## Running the app

Start the app with:

```bash
streamlit run frontend.py
```

This launches the Streamlit interface. The chatbot is initialized from `backend.py` and uses the checkpointed graph for conversation state.

## How the chatbot works

- `backend.py` creates a `ChatState` with a list of messages.
- The `chat_mode` function sends the current message list to the Groq LLM.
- A `StateGraph` compiles the workflow and attaches a SQLite `SqliteSaver` checkpointer.
- `frontend.py` creates a unique `thread_id` per conversation, streams responses, and renders previous messages for the selected thread.
- `chatbot.db` stores the checkpoint and write metadata for each thread.

## Database notes

The SQLite database is created automatically when the app initializes the LangGraph checkpointer. It contains the tables used by LangGraph checkpointing:

- `checkpoints`
- `writes`

These tables store conversation history and state across threads so users can reopen conversations without losing previous messages.

## Usage

- Open the Streamlit app in your browser.
- Type a prompt in the chat box.
- Use the sidebar to start a new conversation or switch between existing thread IDs.
- The app stores and restores previous conversation state based on the selected thread.

## Notes

- The project does not use a separate CLI entrypoint; the app runs through the Streamlit frontend.
- The placeholder entry file was removed to keep the project centered on the actual user-facing app.
