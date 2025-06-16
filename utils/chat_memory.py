from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import streamlit as st

def get_memory(k: int = 5):
    return ConversationBufferWindowMemory(k=k)

def restore_chat_history(memory):
    for message in st.session_state.chat_history:
        memory.save_context({'input': message['human']}, {'output': message['AI']})
        return memory
