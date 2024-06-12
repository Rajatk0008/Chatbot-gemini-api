import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

# Configure the generative AI API with the API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("Google API key not found. Please set it in the .env file.")
else:
    genai.configure(api_key=api_key)

    # Function to load Gemini Pro model and get responses
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    
    def get_gemini_response(question):
        response = chat.send_message(question, stream=True)
        return response

    # Initialize our Streamlit app
    st.set_page_config(page_title="Q&A Demo")

    st.header("Gemini LLM Application")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Text input for user question
    input_text = st.text_input("Input:", key="input")
    submit = st.button("Ask the question")

    if submit and input_text:
        # Check for non-empty input
        if input_text.strip():
            response = get_gemini_response(input_text)
            # Add user query and response to session state chat history
            st.session_state['chat_history'].append(("You", input_text))
            st.subheader(" Response ")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
        else:
            st.warning("Please enter a question.")

    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
