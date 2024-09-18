import uuid
import streamlit as st
from rag import rag
# import db  # Import your database module


def show_ui(prompt_to_user="How may I help you?"):
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]
    
    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = []
    
    if "feedback_message" not in st.session_state:
        st.session_state.feedback_message = ""


    # Generate a unique conversation ID for the session
    conversation_id = str(uuid.uuid4())
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            icon = "👨‍🍳"  # Chef icon
            bg_color = "#f9f9f9"  # Background color for assistant messages
            alignment = "flex-start"  # Align assistant messages to the left
        else:
            icon = "🧑"  # Replace with the desired user icon
            bg_color = "#e1f5fe"  # Background color for user messages
            alignment = "flex-end"  # Align user messages to the right


        st.markdown(f"""
            <div style='display: flex; align-items: flex-start; justify-content: {alignment}; margin-bottom: 10px;'>
                <span style='font-size: 24px;'>{icon}</span>
                <div style='margin-left: 10px; padding: 10px; border-radius: 10px; border: 1px solid #ddd; background-color: {bg_color};'>
                    {message['content']}
                </div>
            </div>
        """, unsafe_allow_html=True)


    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f"""
            <div style='display: flex; align-items: flex-start; justify-content: flex-end; margin-bottom: 10px;'>
                <div style='margin-left: 10px; padding: 10px; border-radius: 10px; border: 1px solid #ddd; background-color: #e1f5fe;'>
                    {prompt}
                </div>
                <span style='font-size: 24px;'>🧑</span>
            </div>
        """, unsafe_allow_html=True)


        # Generate a new response if the last message is not from the assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.spinner("Thinking..."):
                response = rag(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                
                st.markdown(f"""
                    <div style='display: flex; align-items: flex-start; justify-content: flex-start; margin-bottom: 10px;'>
                        <span style='font-size: 24px;'>👨‍🍳</span>
                        <div style='margin-left: 10px; padding: 10px; border-radius: 10px; border: 1px solid #ddd; background-color: #f9f9f9;'>
                            {response['answer']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)


                # Save the conversation to the database
                # db.save_conversation(
                #     conversation_id=conversation_id,
                #     question=prompt,
                #     answer_data=response
                # )


            # Feedback section
            feedback = st.radio("Was this response helpful?", ["Yes", "No"], key="feedback_radio")
            if st.button("Submit Feedback", key="submit_feedback"):
                print(feedback)
                feedback_value = 1 if feedback == "Yes" else -1
                st.session_state.feedbacks.append({"message": response['answer'], "feedback": feedback_value})
                
                # Save the feedback to the database
                # db.save_feedback(
                #     conversation_id=conversation_id,
                #     feedback=feedback_value
                # )
                
                # Display the feedback message
                st.session_state.feedback_message = "Thank you for your feedback!"


    # Display the feedback message
    if st.session_state.feedback_message:
        st.markdown(f"<div style='background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin-top: 20px;'>{st.session_state.feedback_message}</div>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Cook Assistant", page_icon="👨‍🍳")
    st.markdown("<h1 style='text-align: center; color: tomato;'>👨‍🍳 Cook-Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask me anything about recipes, ingredients, and cooking methods!</p>", unsafe_allow_html=True)
    show_ui("What would you like to know?")
    
if __name__ == "__main__":
    main()