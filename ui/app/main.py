import logging

import requests
import streamlit as st
import uuid

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")

API_URL = "http://agents-service:8001/chat"

# Tabs for Chatbot and Data
tab1, tab2 = st.tabs(["🤖 Chatbot", "📊 Data"])

with tab1:
    st.title("🤖 Chatbot")
    st.markdown(
        """
        <style>
        .stChatInputContainer {
            position: fixed;
            bottom: 1.5rem;
            width: 100%;
            background-color: white;
            padding-bottom: 1rem;
            z-index: 999;
        }
        .stChatMessageContainer {
            margin-bottom: 5rem;  /* Leave space for input */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Initialize session state
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.write(f"Session ID: `{st.session_state.session_id}`")
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        st.empty()

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        API_URL,
                        json={
                            "message": prompt,
                            "session_id": st.session_state.session_id,
                        },
                    )
                    response_json = response.json()
                    st.markdown(response_json["message"])

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_json["message"]}
                    )

                except Exception as e:
                    logging.exception("Error")
                    error_message = f"❌ An error occurred: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_message}
                    )
with tab2:
    st.title("📊 Data Management")

    # Text input
    user_input = st.text_input(
        "Fandom url to all pages for your game.",
        placeholder="Ex: " "https://reddead.fandom.com/wiki/Special:AllPages",
    )
    col1, col2, col3 = st.columns(3)

    if "data_output" not in st.session_state:
        st.session_state.data_output = ""

    # Buttons and their actions
    with col1:
        if st.button("🔍 Analyze"):
            st.session_state.data_output = f"Analyzing input: '{user_input}'"

    with col2:
        if st.button("🧹 Clean"):
            st.session_state.data_output = f"Cleaning input: '{user_input.strip()}'"

    with col3:
        if st.button("📤 Export"):
            st.session_state.data_output = f"Exporting data: '{user_input}' (simulated)"

    # Output display
    st.subheader("📄 Output:")
    st.info(st.session_state.data_output or "No output yet.")

# Sidebar with session controls
with st.sidebar:
    st.header("Session Controls")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔄 New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    st.header("Configuration")
    st.text_input(
        "API URL",
        value=API_URL,
        key="api_url_input",
        help="Change this if your Flask app is running on a different URL",
    )

    if st.session_state.api_url_input != API_URL:
        API_URL = st.session_state.api_url_input
