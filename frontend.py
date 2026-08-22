import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat/stream"


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
)


# -----------------------------------
# Custom Styling
# -----------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    section[data-testid="stSidebar"] {
        padding-top: 1rem;
    }

    .stChatInput {
        padding-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------
# Session State
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:

    st.title("🤖 AI Assistant")

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### About")

    st.write(
        "This AI assistant uses FastAPI as the backend "
        "and Groq for language generation."
    )

    st.divider()

    st.caption("Model")
    st.code("openai/gpt-oss-20b")

    st.caption("Backend")
    st.code("FastAPI")

    st.caption("Frontend")
    st.code("Streamlit")


# -----------------------------------
# Header
# -----------------------------------

st.title("🤖 AI Chat Assistant")

st.caption(
    "Ask questions, get explanations, write code, "
    "brainstorm ideas, and more."
)


# -----------------------------------
# Display Chat History
# -----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------------
# User Input
# -----------------------------------

user_message = st.chat_input(
    "Message the AI..."
)


if user_message:

    # -----------------------------------
    # Prepare Previous Conversation
    # -----------------------------------

    history = st.session_state.messages.copy()


    # -----------------------------------
    # Save User Message
    # -----------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    # -----------------------------------
    # Display User Message
    # -----------------------------------

    with st.chat_message("user"):

        st.markdown(user_message)


    # -----------------------------------
    # AI Response
    # -----------------------------------

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""


        try:

            # -----------------------------------
            # Send Streaming Request
            # -----------------------------------

            response = requests.post(
                API_URL,

                json={
                    "message": user_message,

                    "system_prompt": (
                        "You are a helpful AI assistant. "
                        "Do not claim to be ChatGPT or an OpenAI model. "
                        "You are an AI assistant powered by Groq."
                    ),

                    "model": "openai/gpt-oss-20b",

                    "temperature": 0.7,

                    "max_tokens": 300,

                    "history": history,
                },

                stream=True,

                timeout=(10, 120),
            )


            response.raise_for_status()


            # -----------------------------------
            # Receive Streaming Chunks
            # -----------------------------------

            for chunk in response.iter_content(
                chunk_size=None,
                decode_unicode=True,
            ):

                if not chunk:
                    continue


                full_response += chunk


                # -----------------------------------
                # Display Response Immediately
                # -----------------------------------

                message_placeholder.markdown(
                    full_response
                )


            # -----------------------------------
            # Handle Empty Response
            # -----------------------------------

            if not full_response.strip():

                full_response = (
                    "Sorry, I couldn't generate a response."
                )

                message_placeholder.markdown(
                    full_response
                )


            # -----------------------------------
            # Save Assistant Response
            # -----------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                }
            )


        except requests.exceptions.Timeout:

            message_placeholder.error(
                "The AI response took too long. "
                "Please try again."
            )


        except requests.exceptions.ConnectionError:

            message_placeholder.error(
                "Unable to connect to the FastAPI backend. "
                "Please make sure the backend server is running."
            )


        except requests.exceptions.RequestException as e:

            message_placeholder.error(
                "Unable to connect to the AI backend."
            )

            st.caption(str(e))