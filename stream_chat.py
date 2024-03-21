
import streamlit as st
from openai import OpenAI
import time

# Streamlit page configuration
st.set_page_config(page_title='OpenAI Q&A', layout='wide')

def get_response(question):
    client = OpenAI(api_key='your_api_key_here')  # Use Streamlit secrets for the API key

    # Create a thread with the user's question
    thread = client.beta.threads.create(
        messages=[
            {"role": "user", "content": question},
        ]
    )

    # Submit to the assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id='asst_tzLbzTsLkolR7idtVvZvtdVZ')

    # Waiting for the Run to complete
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    # Get the latest message
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    latest_message = message_response.data[0]

    return latest_message.content[0].text.value

# Streamlit UI
st.title('Ask OpenAI')
question = st.text_input('Enter your question:', '')

if st.button('Ask'):
    if question:
        with st.spinner('Waiting for response...'):
            response = get_response(question)
        st.write('Response:', response)
    else:
        st.error('Please enter a question.')
