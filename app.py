
import streamlit as st
from llm import generate_response

st.set_page_config(page_title="AI Storage Assistant", layout="wide")

st.title("AI Storage Intelligence Agent")

# Sidebar: File upload and storage overview


# Main layout: 3 columns (chat, duplicate, compression)
col1, col2, col3 = st.columns([2, 1, 1])

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'duplicate_results' not in st.session_state:
    st.session_state['duplicate_results'] = None
if 'compression_results' not in st.session_state:
    st.session_state['compression_results'] = None

with col1:
    st.header("Assistant Chat")
    # Show conversation above input
    chat_placeholder = st.container()
    with chat_placeholder:
        for role, msg in st.session_state['chat_history']:
            if role == "user":
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**Assistant:** {msg}")
    # Chat input at the bottom
    user_input = st.text_input("Type your message and press Enter", key="chat_input")
    if user_input:
        st.session_state['chat_history'].append(("user", user_input))
        # Build conversation context for LLM
        history_text = "\n".join([
            f"User: {msg}" if role == "user" else f"Assistant: {msg}"
            for role, msg in st.session_state['chat_history']
        ])
        prompt = f"""
You are a helpful AI storage assistant. Use the conversation history to provide relevant, context-aware answers.

Conversation History:
{history_text}

Assistant: """
        assistant_response = generate_response(prompt)
        st.session_state['chat_history'].append(("assistant", assistant_response))
        # Detect if response is about duplicates or compression
        if "duplicate" in assistant_response.lower():
            st.session_state['duplicate_results'] = assistant_response
        if "compress" in assistant_response.lower():
            st.session_state['compression_results'] = assistant_response
        st.rerun()

with col2:
    st.subheader("Duplicate Files")
    if st.session_state['duplicate_results']:
        st.info(st.session_state['duplicate_results'])
    else:
        st.write("No duplicate analysis yet.")

with col3:
    st.subheader("Compression Suggestions")
    if st.session_state['compression_results']:
        st.info(st.session_state['compression_results'])
    else:
        st.write("No compression analysis yet.")

# Run Analysis button (optional future logic)
st.button("Run Storage Analysis")
