import streamlit as st
import sqlite3
import uuid

from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

conn = sqlite3.connect(
    "threads.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS threads(
    thread_id TEXT PRIMARY KEY,
    title TEXT
)
""")

conn.commit()


def create_thread():

    thread_id = str(uuid.uuid4())

    cursor.execute(
        """
        INSERT INTO threads(thread_id,title)
        VALUES(?,?)
        """,
        (
            thread_id,
            "New Chat"
        )
    )

    conn.commit()

    return thread_id


def get_threads():

    cursor.execute(
        """
        SELECT thread_id,title
        FROM threads
        ORDER BY rowid DESC
        """
    )

    return cursor.fetchall()


def update_title(thread_id, title):

    cursor.execute(
        """
        UPDATE threads
        SET title=?
        WHERE thread_id=?
        """,
        (
            title,
            thread_id
        )
    )

    conn.commit()



if "current_thread" not in st.session_state:

    threads = get_threads()

    if len(threads) == 0:
        st.session_state.current_thread = create_thread()
    else:
        st.session_state.current_thread = threads[0][0]


with st.sidebar:

    st.title("Chats")

    if st.button("➕ New Chat"):

        st.session_state.current_thread = create_thread()

        st.rerun()

    st.divider()

    for thread_id, title in get_threads():

        if st.button(
            title,
            key=thread_id
        ):
            st.session_state.current_thread = thread_id
            st.rerun()


config = {
    "configurable": {
        "thread_id": st.session_state.current_thread
    }
}



messages = []

try:

    state = chatbot.get_state(config)

    if state.values:
        messages = state.values.get(
            "messages",
            []
        )

except:
    messages = []



st.title("LangGraph Chatbot")

for message in messages:

    role = (
        "assistant"
        if message.type == "ai"
        else "user"
    )

    with st.chat_message(role):
        st.markdown(message.content)


def stream_response(user_input):

    for msg, metadata in chatbot.stream(
        {
            "messages": [
                HumanMessage(
                    content=user_input
                )
            ]
        },
        config=config,
        stream_mode="messages"
    ):

        if (
            hasattr(msg, "content")
            and msg.content
        ):
            yield msg.content

# --------------------------------
# Input
# --------------------------------

user_input = st.chat_input(
    "Type your message..."
)

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    # First user message becomes title

    current_state = chatbot.get_state(config)

    existing_messages = []

    if current_state.values:
        existing_messages = current_state.values.get(
            "messages",
            []
        )

    if len(existing_messages) == 0:

        update_title(
            st.session_state.current_thread,
            user_input[:30]
        )

    with st.chat_message("assistant"):

        full_response = st.write_stream(
            stream_response(user_input)
        )

    st.rerun()