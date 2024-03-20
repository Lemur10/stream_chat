
import openai
import streamlit as st

st.title("Ask Anything!")

openai.api_key=st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
	st.session_state["openai_model"] = "gpt-4.0-turbo"

#init chat hist
if "messages" not in st.session_state:
	st.session_state.messages=[]

# display chat messages from history on app rerun
for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

#React to user input
prompt = st.chat_input("Ask anything")
if prompt:
	#display user message in message container
	with st.chat_message("user"):
		st.markdown(prompt)

	#add user message to chat history
	st.session_state.messages.append({"role": "user", "content": prompt})

	with st.chat_message("assistant"):
		message_placeholder = st.empty()
		full_response = ""
		for response in openai.ChatCompletion.create(
			model = st.session_state["openai_model"],
			messages=[
				{"role": m["role"], "content": m["content"]}
				for m in st.session_state.messages
			],
			stream=True,
		):

			full_response += response.choices[0].delta.get("content", "")
			message_placeholder.markdown(full_response +"| ")
		message_placeholder.markdown(full_response)
	st.session_state.messages.append({"role": "assistant", "content": full_response})

