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
    conversation_id = str(uuid.uuid4())

    # Initialize session state if not already set
    if 'question' not in st.session_state:
        st.session_state.question = ""

    # Text input for the user's question about cooking
    question = st.text_input("👨‍🍳 What would you like to know today?", st.session_state.question)

    # Process the question
    if question:
        st.session_state.question = question  # Update session state with the current question
        with st.spinner("Cooking up your answer..."):  # Spinner while waiting for the response
            # Call the RAG system to get the answer
            answer_data = rag(question)
        
        # Display the answer in a colorful box
        st.markdown(f"<h2 style='color: darkgreen;'>🍴 Here's your answer:</h2>", unsafe_allow_html=True)
        st.success(answer_data["answer"])

        # Save the conversation in the database
        db.save_conversation(
            conversation_id=conversation_id,
            question=question,
            answer_data=answer_data,
        )

        # Feedback section
        st.markdown("<h3 style='color: darkblue;'>💬 Was the answer helpful?</h3>", unsafe_allow_html=True)
        feedback = st.radio("", ("Yes, it was!", "No, not really."))

        if st.button("Submit Feedback"):
            feedback_value = 1 if feedback == "Yes, it was!" else -1

            # Save the feedback in the database
            # db.save_feedback(
            #     conversation_id=conversation_id,
            #     feedback=feedback_value,
            # )

            # Display feedback result
            st.markdown(f"<p style='color: purple;'>Thank you for your feedback on conversation ID: {conversation_id}!</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
