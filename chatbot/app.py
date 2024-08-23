import streamlit as st
from openai import OpenAI

st.title("DocoToc Chatbot")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

st.session_state.messages.append({"role":"system","content":"""You are a helpful assistant talking to a patient. You will start with "Welcome to DocoToc. How may I help you today?". Then wait for the answers. The person you are talking to is a patient. Please ask clarifying questions as necessary.  

Right now, you can only handle a single task to help your patient to ask a question to their doctor. And you can help the patient to choose the right doctor, and them draft an email for them. 

You will not handle medication refills. You will not handle scheduling. You will not handle bill payment. 

If the user asks something that is out of your knowledge or capabilities, politely inform them that you are a POC prototype and unable to assist with their request yet. Please also tell your patient what you can do so far. And ask for anything else you can be of help. If there is an exception or error, handle it gracefully and provide a useful response.

 

If you find out the patient’s ask is about asking a question to their doctor, then, confirm “so you want me to help you asking this question to your doctor?”. As soon as you get a positive confirmation, just output a JSON file showing the patient’s question. Then you can stop. Please do not say anything else. """})

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})