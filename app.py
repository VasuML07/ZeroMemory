#it lets us to talk to operating sytem so we can get some other things from another files in same folder or file explorer
import os
#streamlit is used for building interactive web interfaces
import streamlit as st
#here we are importing our python api client provider
from groq import Groq
#this loads the secrets securely from env file
#so our api doesn't leak
from dotenv import load_dotenv
#used to read the contents of env file and load it here in this file
load_dotenv()
#here os.getenv reads the variable named from whre it came
#api will create a  api client and attaches our api for every request automatically
#client stores the authenicated keys
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#this one sets page configuration
st.set_page_config(
    page_title="Chat Interface",
    layout="wide"
)
#this one sets the page title
st.title("ZeroMemory")
#this defines a function for user request and input is a string(text)
def get_response(user_message):
    #completion this sends a api request everytime
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        #used for sending user message to model as entire context
        messages=[
            {"role": "user", "content": user_message}
        ],
        #controls the randomness of the prompt
        temperature=0.5,
        #maximum prompt length 512 chars
        max_tokens=512
    )
    #this extracts actual text of model to display on app
    return completion.choices[0].message.content
#creats a chat style input box in ui whatever user types
user_input = st.chat_input("Type your message")
#helps to run after user sends a message
if user_input:
    #display the users message in app
    with st.chat_message("user"):
        st.write(user_input)
    #calls the api and enter user's input
    response = get_response(user_input)
    #it sends the user request and takes model output and shows in app
    with st.chat_message("assistant"):
        st.write(response)  