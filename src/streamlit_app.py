import uuid
import streamlit as st
from rag import rag
import db

# Streamlit app
def main():
    # Add a colorful header with a title for the Cook-Assistant and a chef icon
    st.markdown("<h1 style='text-align: center; color: tomato;'>👨‍🍳 Cook-Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask me anything about recipes, ingredients, and cooking methods!</p>", unsafe_allow_html=True)

    # Generate a conversation ID for each session
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())

    # Initialize session state for question and answer if not already set
    if 'question' not in st.session_state:
        st.session_state.question = ""
    if 'answer' not in st.session_state:
        st.session_state.answer = None

    # Text input for the user's question about cooking, with a unique key
    question = st.text_input("👨‍🍳 What would you like to know today?", st.session_state.question, key=st.session_state.get('input_key', 'input'))
    
    # Handle the "Clear" button press
    if st.button("Clear"):
        # Clear the question and answer from the session state
        st.session_state.question = ""  # Reset the input field
        st.session_state.answer = None  # Clear the answer
        st.session_state.input_key = str(uuid.uuid4())  # Reset the key for the input field
        st.rerun()  # Rerun the app to update the UI

    
    # Process the question if it's not empty
    if question and st.session_state.answer is None:
        st.session_state.question = question  # Update session state with the current question
        with st.spinner("Cooking up your answer..."):  # Spinner while waiting for the response
            # Call the RAG system to get the answer
            answer_data = rag(question)
            st.session_state.answer = answer_data  # Save the answer in session state
        
    # Display the answer if available
    if st.session_state.answer:
        st.markdown(f"<h2 style='color: darkgreen;'>🍴 Here's your answer:</h2>", unsafe_allow_html=True)
        st.success(st.session_state.answer["answer"])

        # Save the conversation in the database
        db.save_conversation(
            conversation_id=st.session_state.conversation_id,
            question=st.session_state.question,
            answer_data=st.session_state.answer,
        )

        # Feedback section
        st.markdown("<h3 style='color: darkblue;'>💬 Was the answer helpful?</h3>", unsafe_allow_html=True)
        feedback = st.radio("Feedback", ("Yes, it was!", "No, not really."), label_visibility="collapsed")

        if st.button("Submit Feedback"):
            feedback_value = 1 if feedback == "Yes, it was!" else -1

            # Save the feedback in the database
            db.save_feedback(
                conversation_id=st.session_state.conversation_id,
                feedback=feedback_value,
            )

            # Display feedback result
            st.markdown(f"<p style='color: purple;'>Thank you for your feedback on conversation ID: {st.session_state.conversation_id}!</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
