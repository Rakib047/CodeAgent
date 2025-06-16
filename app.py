import streamlit as st
from dotenv import load_dotenv
 
from utils.chat_memory import get_memory, restore_chat_history 
from ui.side_bar import make_side_bar
from ui.body import main_body

load_dotenv() 
def main(): 
    setting = make_side_bar()


    spacer, col = st.columns([5, 1])
    with col:
        st.image('assets/groq_image.png')

    st.title('Chat with Groq!')
    st.write("I'm your friendly Chatbot")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    memory = get_memory(setting['memory_length'])
    memory = restore_chat_history(memory)

    main_body(memory, setting)



if __name__ == "__main__":
    main()
