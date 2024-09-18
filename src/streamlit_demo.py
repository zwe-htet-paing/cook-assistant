import uuid
import streamlit as st
from rag import rag
# import db  # Import your database module

def show_ui(prompt_to_user="How may I help you?"):
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]
        st.session_state.feedback_visible = {}  # Dictionary to track visibility of feedback options
        st.session_state.feedback_storage = {}  # Dictionary to store feedback
        st.session_state.thank_you_visible = {}  # Dictionary to track visibility of thank you messages    
    
    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        if message["role"] == "assistant":
            icon = "👨‍🍳"  # Chef icon
            bg_color = "#f9f9f9"  # Background color for assistant messages
            alignment = "flex-start"  # Align assistant messages to the left
        else:
            icon = "🧑"  # User icon
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

        # Show feedback options only for responses after the initial prompt
        if message["role"] == "assistant":
            feedback_key = f"feedback_{idx}"
            thank_you_key = f"thank_you_{idx}"

            if st.session_state.feedback_visible.get(idx, False):
                # Display feedback radio buttons
                selected_feedback = st.radio(
                    "Was this response helpful?", 
                    ['👍', '👎'], 
                    horizontal=True,
                    key=feedback_key  # Unique key to manage state
                )
                # Handle submit feedback
                submit_key = f"submit_{idx}"
                if st.button("Submit Feedback", key=submit_key):
                    st.session_state.feedback_storage[idx] = selected_feedback
                    st.session_state.feedback_visible[idx] = False  # Hide feedback for this specific response
                    st.session_state.thank_you_visible[idx] = True  # Show thank you message
                    feedback_value = 1 if selected_feedback == "👍" else -1
                    # Save the feedback to the database
                    # db.save_feedback(
                    #     conversation_id=message["id"],
                    #     feedback=feedback_value
                    # )
                    # Optionally, you can use st.rerun() to re-render the UI
                    st.rerun()

            if st.session_state.thank_you_visible.get(idx, False):
                st.markdown("<p style='color: green;'>Thank you for your feedback!</p>", unsafe_allow_html=True)

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

        # Generate a new response from the assistant
        with st.spinner("Thinking..."):
            response = rag(prompt)
            conversation_id = str(uuid.uuid4())
            st.markdown(f"""
                <div style='display: flex; align-items: flex-start; justify-content: flex-start; margin-bottom: 10px;'>
                    <span style='font-size: 24px;'>👨‍🍳</span>
                    <div style='margin-left: 10px; padding: 10px; border-radius: 10px; border: 1px solid #ddd; background-color: #f9f9f9;'>
                        {response['answer']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # # Save the conversation to the database
            # db.save_conversation(
            #     conversation_id=conversation_id,
            #     question=prompt,
            #     answer_data=response
            # )
        
        # Add the assistant's response to the session state
        st.session_state.messages.append({"role": "assistant", "content": response['answer'], "id": conversation_id})

        # Show feedback options after generating a new response
        st.session_state.feedback_visible[len(st.session_state.messages) - 1] = True
        st.session_state.thank_you_visible[len(st.session_state.messages) - 1] = False
        st.rerun()  # Re-render the UI to display feedback options

def main():
    st.set_page_config(page_title="Cook Assistant", page_icon="👨‍🍳")
    # Add a colorful header with a title for the Cook-Assistant and a chef icon
    st.markdown("<h1 style='text-align: center; color: tomato;'>👨‍🍳 Cook-Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask me anything about recipes, ingredients, and cooking methods!</p>", unsafe_allow_html=True)
    show_ui("What would you like to know?")
    
if __name__ == "__main__":
    main()
