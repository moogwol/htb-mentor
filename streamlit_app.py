import streamlit as st

from database.conversations import get_all_conversations
from database.messages import get_messages
from app.chat import send_message

# Set page configuration
st.set_page_config(
    page_title="HTB Mentor",
    page_icon="🤖",
    layout="wide"
    )

st.title("HTB Mentor")

conversations = get_all_conversations()

st.sidebar.header("Conversations")

if conversations:
    conversation_options = {
        f"{c['title']} (ID: {c['id']})": c['id']
        for c in conversations
    }
    
    selected_conversation = st.sidebar.selectbox(
        "Select a conversation",
        options=list(conversation_options.keys()),
    )
    
    conversation_id = conversation_options[selected_conversation]   
    
    st.write(f"Selected Conversation: {selected_conversation}")
    
else:
    st.sidebar.write("No conversations found.")
    
    
# load conversation history
if conversation_id:
    messages = get_messages(conversation_id)
    st. header(selected_conversation)   
    
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])    
            
# Create a text input for the user to type their message
prompt = st.chat_input("Salaam, what is your question master?...")

if prompt:
    # Display the user's message in the chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


    # Display the assistant's response in the chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = send_message(conversation_id, prompt)

        st.markdown(response)            