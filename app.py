
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
if 'user_profile' not in st.session_state:
    st.session_state['user_profile'] = {}

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
    def handle_chat_submit():
        user_input = st.session_state['chat_input']
        if user_input:
            st.session_state['chat_history'].append(("user", user_input))
            # Extract user profile info from input
            import re
            profile = st.session_state['user_profile']
            name_match = re.search(r"my name is ([\w\s]+)", user_input, re.IGNORECASE)
            color_match = re.search(r"my favourite color is ([\w\s]+)", user_input, re.IGNORECASE)
            track_match = re.search(r"my hackathon track is ([\w\s]+)", user_input, re.IGNORECASE)
            if name_match:
                profile['name'] = name_match.group(1).strip()
            if color_match:
                profile['color'] = color_match.group(1).strip()
            if track_match:
                profile['track'] = track_match.group(1).strip()
            st.session_state['user_profile'] = profile

            # Build user profile text
            profile_text = "\n".join([
                f"Name: {profile['name']}" if 'name' in profile else "",
                f"Favorite color: {profile['color']}" if 'color' in profile else "",
                f"Hackathon track: {profile['track']}" if 'track' in profile else ""
            ]).strip()

            # Build conversation context for LLM
            history_text = "\n".join([
                f"User: {msg}" if role == "user" else f"Assistant: {msg}"
                for role, msg in st.session_state['chat_history']
            ])
            prompt = f"""
You are a helpful, context-aware AI storage assistant. Use the user profile and conversation history to provide relevant, personal answers. Do NOT say you don't have access to memory—use the chat history and profile info.

User Profile:
{profile_text}

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
            # Clear input after submission to prevent repeated sending
            st.session_state['chat_input'] = ""

    st.text_input(
        "Type your message and press Enter",
        key="chat_input",
        on_change=handle_chat_submit
    )

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
