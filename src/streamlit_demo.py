import uuid
import streamlit as st
from rag import rag

def show_ui(prompt_to_user="How may I help you?"):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = rag(prompt)
                st.markdown(response['answer'])
        message = {"role": "assistant", "content": response['answer']}
        st.session_state.messages.append(message)
        
        
def main():
    st.set_page_config(page_title="Cook Assistant", page_icon="👨‍🍳")
    # st.title("Streamlit RAG")
    # Add a colorful header with a title for the Cook-Assistant and a chef icon
    st.markdown("<h1 style='text-align: center; color: tomato;'>👨‍🍳 Cook-Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask me anything about recipes, ingredients, and cooking methods!</p>", unsafe_allow_html=True)
    show_ui("What would you like to know?")
    
if __name__ == "__main__":
    main()