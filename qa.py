from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
chat = model.start_chat(history=[])

def get_response(query):
    resp = chat.send_message(query, stream=True)
    return resp

st.set_page_config(page_title="Chat Demo")
st.header("Q&A Companion")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and user_input:
    resp = get_response(user_input)
    st.session_state['chat_history'].append(("You", user_input))
    st.subheader("Response:")
    response_text = ""
    for chunk in resp:
        st.write(chunk.text)
        response_text += chunk.text
    st.session_state['chat_history'].append(("Companion", response_text))

st.subheader("Chat History:")
for user, text in st.session_state['chat_history']:
    st.write(f"**{user}:** {text}")
