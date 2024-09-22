import uuid
import streamlit as st
import requests

def ask_question(url, question):
    data = {"question": question}
    response = requests.post(url, json=data)
    return response.json()

def send_feedback(url, conversation_id, feedback):
    feedback_data = {"conversation_id": conversation_id, "feedback": feedback}
    response = requests.post(f"{url}/feedback", json=feedback_data)
    return response.status_code

# Streamlit app
def main():
    # Add a colorful header with a title for the Cook-Assistant and a chef icon
    st.markdown("<h1 style='text-align: center; color: tomato;'>👨‍🍳 Cook-Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask me anything about recipes, ingredients, and cooking methods!</p>", unsafe_allow_html=True)

    # Initialize session state for question and answer if not already set
    if 'question' not in st.session_state:
        st.session_state.question = ""
    if 'answer' not in st.session_state:
        st.session_state.answer = None
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = None

    # Text input for the user's question about cooking, with a unique key
    question = st.text_area("👨‍🍳 What would you like to know today?", st.session_state.question, key=st.session_state.get('input_key', 'input'))
    
    # Handle the "Clear" button press
    if st.button("Clear"):
        # Clear the question and answer from the session state
        st.session_state.question = ""  # Reset the input field
        st.session_state.answer = None  # Clear the answer
        st.session_state.input_key = None # Reset the key for the input field
        st.rerun()  # Rerun the app to update the UI

    base_url = "http://localhost:5000"
    
    # Process the question if it's not empty
    if question and st.session_state.answer is None:
        st.session_state.question = question  # Update session state with the current question
        with st.spinner("Cooking up your answer..."):  # Spinner while waiting for the response
            response = ask_question(f"{base_url}/question", question)
            print(question)
            st.session_state.conversation_id = response.get("conversation_id", str(uuid.uuid4()))
            st.session_state.answer = response  # Save the answer in session state
        
    # Display the answer if available
    if st.session_state.answer:
        st.markdown(f"<h2 style='color: darkgreen;'>🍴 Here's your answer:</h2>", unsafe_allow_html=True)
        st.success(st.session_state.answer["answer"])
        
        # Feedback section
        st.markdown("<h4 style='color: darkblue;'>💬 Was the answer helpful?</h4>", unsafe_allow_html=True)
        feedback = st.radio("Feedback", ("Yes, it was!", "No, not really."), label_visibility="collapsed")

        status = None
        if st.button("Submit Feedback"):
            feedback_value = 1 if feedback == "Yes, it was!" else -1
            status = send_feedback(base_url, st.session_state.conversation_id, feedback_value)
            
        # Display feedback result
        if status == 200:
            st.markdown(f"<p style='color: purple;'>Thank you for your feedback on conversation ID: {st.session_state.conversation_id}!</p>", unsafe_allow_html=True)
            # st.rerun()

if __name__ == "__main__":
    main()
