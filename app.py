from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os

import google.generativeai as genai

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

# Function to load Gemini Pro model and get response

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history = [])


def get_gemini_response(question):
    response = chat.send_message(question, stream = True)
    return response

st.set_page_config(page_title = 'Gemini Q&A chatbot')

st.header('Gemini Conversational chatbot')

# Intitialize session state for chat history if it doesn't exist

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input('Input:', key = 'input')
submit = st.button('Ask the question')

if submit and input:
    response = get_gemini_response(input)
    
    # Add user query and response in chat history
    st.session_state['chat_history'].append(('you', input))
    st.subheader('The Response is') 

    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('Chatbot', chunk.text))

st.subheader('The chat history is here')

for role, text in st.session_state['chat_history']:
    st.write(f'{role}: {text}')

