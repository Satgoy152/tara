import streamlit as st
import time
from chat_responses import LMMentorBot
from audit_parse import extract_text_fromaudit
from feedback import append_values

st.set_page_config(
    page_title="Tara", 
    page_icon=":sparkles:", 
    layout="centered")
st.title("✨ Talk to Tara - University of Michigan")

with st.sidebar:
    st.header("Meet Tara or your Tailored Academic & Resource Assistant!")
    st.write("To get started you can either start chatting with Tara or simply upload your Degree Audit Checklist or Report pdf.")
    st.info("Download Audit from: Wolverine Access > Backpack > My Academics > View My Advisement Report > Checklist Report PDF.")
    st.divider()
    st.write("Tara can help you with:")
    st.write("- Degree Audit Summary and Breakdown")
    st.write("- Course Recommendations")
    st.write("- Resources for Academic Success")
    st.divider()
    with st.expander("Disclaimer", icon ="⚠️"):
        st.markdown("Tara is a virtual assistant and is **not** a replacement for academic advisors. Please consult with your academic advisor for official advice.")
        st.write("Tara does not store any personal information, any feedback is anonymous.")


# Initialize chat bot
if "chatBot" not in st.session_state:
    st.session_state.chatBot = LMMentorBot()


# Initialize degree audit boolean
if "degree_audit" not in st.session_state:
    st.session_state.degree_audit = False


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamed response emulator
def response_generator(text):

    # call chat bot
    response = st.session_state.chatBot.chat(text)

    # if line break in response go to next line
    for word in response.split(" "):
        if word == "":
            yield word + " "
        else:
            yield word + " "
            time.sleep(0.06)

def audit_response_generator(text):

    # call chat bot
    response = st.session_state.chatBot.upload_degree_audit(text)

    # if line break in response go to next line
    for word in response.split(" "):
        if word == "":
            yield word + " "
        else:
            yield word + " "
            time.sleep(0.06)

def send_user_input(prompt:str):
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
    
    # add to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # call response generator
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Thinking..."):
            response = st.write_stream(response_generator(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})

uploaded_file = st.file_uploader("Upload your Degree Audit here:", type=["pdf"], accept_multiple_files=False)
# add file drop
if uploaded_file is None:
    st.session_state.degree_audit = False

# Display chat messages from history
for message in st.session_state.messages:
    avatar = None
    if message["role"] == "user":
        avatar = "🧑‍🎓"
    else:
        avatar = "✨"
        
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

if uploaded_file is not None and st.session_state.degree_audit == False:
    audit_text = extract_text_fromaudit(uploaded_file)

    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown("*You uploaded your degree audit*")
    
    if audit_text == "":
        st.error("Error extracting text from PDF. Please try again.")
        st.stop()
    if audit_text == "Invalid PDF":
        st.error("This doesn't look like a degree audit. Please try again.")
        st.stop()
    
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Analyzing your Degree Audit..."):
            response = st.write_stream(audit_response_generator(audit_text))
    
    
    # add to chat history
    st.session_state.messages.append({"role": "user", "content": "*You uploaded your degree audit*"})

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.degree_audit = True


# Get user input
if prompt := st.chat_input("What classes should I take if I want to become...?"):
    # Display user message
    send_user_input(prompt)

    # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
selected = st.feedback("thumbs")
if selected is not None:
    sentiment = None
    if selected == 0:
        sentiment = "Negative"
    else:
        sentiment = "Positive"
    append_values("1WAuUGd130tEnsjFzaYy7Tgq5H3zh-vvp7WXlg9WPNAs", "Sheet1!A1:C1", "USER_ENTERED", [["Session id: Test", str(st.session_state.messages), sentiment]])
    st.success("Thank you for your feedback!")
