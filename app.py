import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import fitz  # PyMuPDF for reading PDF files

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
    
    def get_gemini_response(question, context=None):
        if context:
            question = f"{question}\nContext: {context}"
        response = chat.send_message(question, stream=True)
        return response

    def extract_text_from_pdf(pdf_file):
        text = ""
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

    # Initialize our Streamlit app
    st.set_page_config(page_title="Q&A Demo")
    st.header("Gemini LLM Application")

    # Initialize session state for chat history and PDF context if they don't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'pdf_text' not in st.session_state:
        st.session_state['pdf_text'] = None

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        st.session_state['pdf_text'] = extract_text_from_pdf(uploaded_file)
        st.success("PDF uploaded and processed successfully.")

    # Text input for user question
    input_text = st.text_input("Input:", key="input")
    submit = st.button("Ask the question")

    if submit and input_text:
        # Check for non-empty input
        if input_text.strip():
            context = st.session_state['pdf_text']
            response = get_gemini_response(input_text, context)
            # Add user query and response to session state chat history
            st.session_state['chat_history'].append(("You", input_text))
            st.subheader("Response")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
        else:
            st.warning("Please enter a question.")

    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
