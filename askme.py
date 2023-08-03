
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
from langchain.llms.openai import OpenAI

from llama_index import (
    PromptHelper,
    load_index_from_storage,
    ServiceContext,
    StorageContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.llms import ChatMessage, OpenAI

service_context = ServiceContext.from_defaults(
    #todo repalce with llamma2
    llm=OpenAI(model="gpt-3.5-turbo", temperature=0) 
)

# messages = [
#     ChatMessage(role="system", content="You are a pirate with a colorful personality"),
#     ChatMessage(role="user", content="What is your name"),
# ]
# max_input_size = 4096
# num_output = 256
# max_chunk_overlap = 20
# prompt_helper = PromptHelper(max_input_size, num_output)


# storage_context = StorageContext.from_defaults()
# data = SimpleDirectoryReader(input_dir="C:\\dev\\llama_index\\examples\\dk").load_data()
# index = VectorStoreIndex.from_documents(
#     data, 
#     service_context=service_context,         
#     storage_context=storage_context, 
#     show_progress=True
# )
# storage_context.persist(persist_dir=f'./storage/myth')


storage_context = StorageContext.from_defaults(persist_dir=f'./storage/myth')
index = load_index_from_storage(storage_context=storage_context)

# Configure chat engine
chat_engine = index.as_chat_engine(
    chat_mode="react", verbose=True
)  # react , best or context ?

# Define a simple Streamlit app

st.set_page_config(
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
	page_title="denisaBot",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="fav.png",  # String, anything supported by st.image, or None.
)

st.title('What would you like to ask the book "Algorithms and Automation"?')
query = st.text_input(
     'Examples: "What is a prototype, and how is it relevant to philosophical discussions?"', ""
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
