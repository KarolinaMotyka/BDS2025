import streamlit as st
import requests
import uuid

API_URL = "http://localhost:3000/api/v1/prediction/18f1f6c6-70bd-42b0-808b-52f39f4a2965"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

# Function to start a new chat session
def start_new_chat():
    st.session_state['messages'] = []
    st.session_state['chat_id'] = str(uuid.uuid4())
    st.session_state['session_id'] = str(uuid.uuid4())
    st.session_state['chat_message_id'] = None
    st.success("🆕 New chat session started!")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'chat_id' not in st.session_state:
    st.session_state['chat_id'] = str(uuid.uuid4())
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
if 'chat_message_id' not in st.session_state:
    st.session_state['chat_message_id'] = None  # Will be set when sending a message

# Main Title - Introduction
st.title("🤖 Virtual Assistant")

st.markdown("""
Welcome! I am your **Virtual Assistant**. Here's what I can help you with:
- 💬 **General Questions:** Ask me anything, and I’ll provide an answer. I can even search the web 🌐.
- 🧮 **Calculator:** Perform simple calculations directly within the app.
- 📄 **Document Questions:** Ask me questions related to any document.

Use the appropriate section for your query or type directly in the chat window at the bottom!
""")

# Clear chat history and start a new chat
if st.button("🗑️ Clear Chat History and Start New Chat"):
    start_new_chat()

# Display chat history
st.header("💬 Chat History")
for message in st.session_state['messages']:
    role = message['role'].lower()
    if role == 'user':
        with st.chat_message("user"):
            st.write(message['content'])
    else:
        with st.chat_message("assistant"):
            st.write(message['content'])

# Section 1: General Questions
st.header("💬 General Questions")
general_input = st.text_input("Ask a general question...", key="general_input")
if st.button("Send General Question"):
    if general_input.strip():
        st.session_state['chat_message_id'] = str(uuid.uuid4())
        st.session_state['messages'].append({'role': 'user', 'content': general_input})
        with st.chat_message("user"):
            st.write(general_input)

        payload = {
            "question": general_input,
            "chatId": st.session_state['chat_id'],
            "sessionId": st.session_state['session_id'],
            "chatMessageId": st.session_state['chat_message_id'],
        }

        try:
            data = query(payload)
            bot_reply = data.get('text', 'No response from the assistant.')
            st.session_state['messages'].append({'role': 'assistant', 'content': bot_reply})
            with st.chat_message("assistant"):
                st.write(bot_reply)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a general question.")

# Section 2: Calculator
st.header("🧮 Calculator")
calc_input = st.text_input("Enter a calculation (e.g., 5 + 3 * 2):", key="calculator_input")
if st.button("Calculate"):
    if calc_input.strip():
        st.session_state['chat_message_id'] = str(uuid.uuid4())
        st.session_state['messages'].append({'role': 'user', 'content': calc_input})
        with st.chat_message("user"):
            st.write(calc_input)

        payload = {
            "question": calc_input,
            "chatId": st.session_state['chat_id'],
            "sessionId": st.session_state['session_id'],
            "chatMessageId": st.session_state['chat_message_id'],
        }

        try:
            data = query(payload)
            calc_result = data.get('text', 'No response from the assistant.')
            st.session_state['messages'].append({'role': 'assistant', 'content': calc_result})
            with st.chat_message("assistant"):
                st.write(calc_result)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid calculation.")

# Section 3: Document Questions
st.header("📄 Document Questions")
doc_question = st.text_input("Ask a document-related question...", key="document_input")
if st.button("Submit Document Question"):
    if doc_question.strip():
        st.session_state['chat_message_id'] = str(uuid.uuid4())
        st.session_state['messages'].append({'role': 'user', 'content': doc_question})
        with st.chat_message("user"):
            st.write(doc_question)

        payload = {
            "question": doc_question,
            "chatId": st.session_state['chat_id'],
            "sessionId": st.session_state['session_id'],
            "chatMessageId": st.session_state['chat_message_id'],
        }

        try:
            data = query(payload)
            doc_reply = data.get('text', 'No response from the assistant.')
            st.session_state['messages'].append({'role': 'assistant', 'content': doc_reply})
            with st.chat_message("assistant"):
                st.write(doc_reply)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a document-related question.")

# 🔥 Unified Input at the Bottom for All Queries
st.header("💡 Quick Question Input")
user_input = st.chat_input("Ask me anything (general, calculation, or document-related)...", key="unified_input")
if user_input:
    user_input = user_input.strip()
    if user_input:
        st.session_state['chat_message_id'] = str(uuid.uuid4())
        st.session_state['messages'].append({'role': 'user', 'content': user_input})
        with st.chat_message("user"):
            st.write(user_input)

        payload = {
            "question": user_input,
            "chatId": st.session_state['chat_id'],
            "sessionId": st.session_state['session_id'],
            "chatMessageId": st.session_state['chat_message_id'],
        }

        try:
            data = query(payload)
            bot_reply = data.get('text', 'No response from the assistant.')
            st.session_state['messages'].append({'role': 'assistant', 'content': bot_reply})
            with st.chat_message("assistant"):
                st.write(bot_reply)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
