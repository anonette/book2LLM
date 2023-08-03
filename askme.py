
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import streamlit as st
from langchain.llms.openai import OpenAI

from llama_index import (
    PromptHelper,
    ServiceContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.llms import ChatMessage, OpenAI

service_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-3.5-turbo", temperature=0)
)
# messages = [
#     ChatMessage(role="system", content="You are a pirate with a colorful personality"),
#     ChatMessage(role="user", content="What is your name"),
# ]
max_input_size = 4096
num_output = 256
max_chunk_overlap = 20
prompt_helper = PromptHelper(max_input_size, num_output)

data = SimpleDirectoryReader(input_dir="C:\dev\llama_index\examples\dk").load_data()
index = VectorStoreIndex.from_documents(data, service_context=service_context)

# Configure chat engine
chat_engine = index.as_chat_engine(
    chat_mode="react", verbose=True
)  # react , best or context ?

# Define a simple Streamlit app
st.title("Ask Denisa")
query = st.text_input(
    "What would you like to ask? (source: Algorithms and Automation)", ""
)

# If the 'Submit' button is clicked
if st.button("Submit"):
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            response = chat_engine.query(query)
            st.success(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
