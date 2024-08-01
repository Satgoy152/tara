import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random
from chat_responses import LMMentorBot

st.set_page_config(
    page_title="LM Mentor", 
    page_icon=":student:", 
    layout="wide")

st.title("University of Michigan LM Mentor")
st.header("Welcome to LM Mentor, your academic companion!")

# add file drop
uploaded_file = st.file_uploader("Upload your Degree Audit", type=["pdf"], accept_multiple_files=True)

# Initialize chat bot
if "chatBot" not in st.session_state:
    st.session_state.chatBot = LMMentorBot()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Streamed response emulator
def response_generator(text):

    # call chat bot
    response = st.session_state.chatBot.chat(text)
    print(response)

    # if line break in response go to next line
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.06)


# Get user input
if prompt := st.chat_input("How is my degree progress?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # add to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # call response generator
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})

# Display assistant response in chat message container
# with st.chat_message("assistant"):
#     response = st.write_stream(response_generator(prompt))
# Add assistant response to chat history
