


import os
import json
import random
import argparse
import streamlit as st
import openai
from langchain.llms.openai import OpenAI
from llama_index import (PromptHelper, load_index_from_storage, ServiceContext,
                         StorageContext, SimpleDirectoryReader, VectorStoreIndex)
from llama_index.llms import ChatMessage

# Load environment variables from .streamlit/secrets.json

# Define constants
PAGE_TITLE = "denisaBot"
PAGE_ICON = "fav.png"
PERSIST_DIR = './storage/myth'
INPUT_DIR = "data/"
QUESTION_FILE = "questions/merged_fix.json"

# Define Streamlit app settings
st.set_page_config(
    layout="centered",
    initial_sidebar_state="auto",
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON
    )

# Initialize ServiceContext
service_context = ServiceContext.from_defaults(
    llm=OpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        streaming=False),
        prompt_helper=PromptHelper
    )

# Handle command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    '--mode',
    choices=['write', 'read'],
    help='Mode to run the script in: write or read',
    default='read'
    )
args = parser.parse_args()

def write_to_index():
    storage_context = StorageContext.from_defaults()
    data = SimpleDirectoryReader(input_dir=INPUT_DIR).load_data()
    index = VectorStoreIndex.from_documents(
        data,
        service_context=service_context,
        storage_context=storage_context,
        show_progress=True
        )
    storage_context.persist(persist_dir=PERSIST_DIR)
    return index

@st.cache_resource
def read_from_index():
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context=storage_context)
    return index

class RandomQuestionGenerator:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)

        # Flatten the JSON structure to get a list of all questions
        self.all_questions = [
            q['question']
            for title_block in data
            if 'paragraphs' in title_block
            for paragraph in title_block['paragraphs']
            if 'questions' in paragraph
            for q in paragraph['questions']
        ]

        # Convert the list to a set for non-repetitive random selection
        self.questions_set = set(self.all_questions)

    def get_random_question(self):
        if not self.questions_set:
            # Refill the set if all questions have been asked
            self.questions_set = set(self.all_questions)

        question = random.choice(list(self.questions_set))
        self.questions_set.remove(question)
        return question

# If 'generator' not in session state, initialize it
if 'generator' not in st.session_state:
    # Initialize RandomQuestionGenerator
    st.session_state['generator'] = RandomQuestionGenerator(QUESTION_FILE)

# If 'index' not in session state, load it

index = write_to_index() if args.mode == 'write' else read_from_index()

# Get the current query from session state or set a placeholder if it's not yet set
if 'current_query' not in st.session_state:
    st.session_state['current_query'] = st.session_state['generator'].get_random_question()

# Configure chat engine
chat_engine = index.as_chat_engine(
    chat_mode="react",
    verbose=True
    )



# Define Streamlit layout
st.title('What would ask the book "Algorithms and Automation"?')

# Get the current query from session state or set a placeholder if it's not yet set
current_query = st.session_state.get('current_query', '')

query = st.text_area(
    'enter a question or submit one from the archives:', '',
    placeholder=current_query
    )

# Define Streamlit buttons
col1, col2 , col3, col4= st.columns(4)

if col1.button("Submit"):
    if not query.strip():
        query = current_query
    try:
        response = chat_engine.query(query)
        # print(response)
        st.success(f"Question: {query}\n\n\nAnswer: {response}")
        # for token in response.response_gen:
        #     st.write(token)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

if col4.button("random question"):
    st.session_state['current_query'] = st.session_state['generator'].get_random_question() # Update the session state with a new random question
    st.experimental_rerun()

footer="""<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class="footer">
<p>for questions, write to algorithms.automation[at]gmail by <a href="https://www.anonnete.net/" target="_blank">denisa kera</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
