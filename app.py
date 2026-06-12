import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

st.set_page_config(page_title="Prompt Playground")

st.title("🧠 Prompt Playground")

question = st.text_area(
    "Ask a question",
    placeholder="How do I learn Python?"
)

def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ask_model(system_prompt, user_message):

    messages = []

    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    response = client.chat.completions.create(
        model="gpt-5",
        messages=messages
    )

    return response.choices[0].message.content

if st.button("Compare Prompts"):

    if not question:
        st.warning("Enter a question first.")
        st.stop()

    assistant_prompt = load_prompt(
        "prompts/assistant.txt"
    )

    programmer_prompt = load_prompt(
        "prompts/programmer.txt"
    )

    with st.spinner("Generating responses..."):

        response_1 = ask_model(
            "",
            question
        )

        response_2 = ask_model(
            assistant_prompt,
            question
        )

        response_3 = ask_model(
            programmer_prompt,
            question
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("No Prompt")
        st.write(response_1)

    with col2:
        st.subheader("Assistant Prompt")
        st.write(response_2)

    with col3:
        st.subheader("Programmer Prompt")
        st.write(response_3)
