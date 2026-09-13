import requests
import streamlit as st


API_URL = "https://llm-backend-service-production.up.railway.app"


st.set_page_config(
    page_title="LLM Chat",
    page_icon="🤖",
    layout="centered",
)


st.title("🤖 LLM Chat Assistant")
st.write("Chat with the LLM Backend Service")


# -------------------------
# Session State
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# Sidebar Settings
# -------------------------

st.sidebar.header("Chat Settings")

model = st.sidebar.selectbox(
    "Model",
    ["openai/gpt-oss-20b"],
)

system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="You are a helpful assistant.",
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
)

max_tokens = st.sidebar.number_input(
    "Max Tokens",
    min_value=1,
    max_value=4000,
    value=300,
    step=50,
)


# -------------------------
# Clear Chat
# -------------------------

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# -------------------------
# Display Previous Messages
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -------------------------
# Chat Input
# -------------------------

message = st.chat_input("Type your message...")


if message:

    # Show user message
    with st.chat_message("user"):
        st.write(message)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    # -------------------------
    # Prepare Payload
    # -------------------------

    payload = {
        "message": message,
        "system_prompt": system_prompt,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "history": st.session_state.messages[:-1],
    }

    try:

        with st.spinner("Connecting to LLM..."):

            response = requests.post(
                f"{API_URL}/chat/stream",
                json=payload,
                timeout=60,
                stream=True,
            )

        # -------------------------
        # Streaming Response
        # -------------------------

        if response.status_code == 200:

            assistant_response = ""

            with st.chat_message("assistant"):

                response_placeholder = st.empty()

                for chunk in response.iter_content(
                    chunk_size=None,
                    decode_unicode=True,
                ):

                    if chunk:

                        assistant_response += chunk

                        response_placeholder.markdown(
                            assistant_response
                        )

            # Save assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_response,
                }
            )

        else:

            st.error(
                f"Backend error ({response.status_code}): "
                f"{response.text}"
            )

    except requests.exceptions.RequestException as exc:

        st.error(
            f"Could not connect to the backend: {exc}"
        )
