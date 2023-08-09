import os
import json
import random
import argparse
import streamlit as st
from dotenv import load_dotenv
from langchain.llms.openai import OpenAI
from llama_index import (PromptHelper, load_index_from_storage, ServiceContext,
                         StorageContext, SimpleDirectoryReader, VectorStoreIndex)
from llama_index.llms import ChatMessage

# Load environment variables
load_dotenv()

# constants
PAGE_TITLE = "denisaBot"
PAGE_ICON = "fav.png"
PERSIST_DIR = './storage/myth'
INPUT_DIR = "data/"
QUESTION_FILE = "questions/merged_fix.json"

# Initialize ServiceContext
service_context = ServiceContext.from_defaults(
    llm=OpenAI(
        model="gpt-3.5-turbo", 
        temperature=0)
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

def read_from_index():
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context=storage_context)
    return index

# Switch between write and read mode
index = write_to_index() if args.mode == 'write' else read_from_index()

# Configure chat engine
chat_engine = index.as_chat_engine(chat_mode="react", verbose=True)

# Define Streamlit app settings
st.set_page_config(
    layout="centered", 
    initial_sidebar_state="auto", 
    page_title=PAGE_TITLE, 
    page_icon=PAGE_ICON
    )

class RandomQuestionGenerator:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            self.data = json.load(f)

    def get_random_question(self):
        while True:
            random_title_block = random.choice(self.data)
            if 'paragraphs' in random_title_block and random_title_block['paragraphs']:
                random_paragraph = random.choice(random_title_block['paragraphs'])
                if 'questions' in random_paragraph and random_paragraph['questions']:
                    random_question = random.choice(random_paragraph['questions'])
                    return random_question['question']

# Initialize RandomQuestionGenerator
generator = RandomQuestionGenerator(QUESTION_FILE)

# Initialize Session State if it doesn't exist
if 'random_question' not in st.session_state:
    st.session_state['random_question'] = generator.get_random_question()

# Define Streamlit layout
st.title('What would you like to ask the book "Algorithms and Automation"?')
query = st.text_area(
    'enter a question or submit one from the archives:', 
    '', 
    placeholder=st.session_state["random_question"]
    )

# Define Streamlit buttons
col1, col2 , col3, col4= st.columns(4)

if col1.button("Submit"):
    if not query.strip():
        query = st.session_state['random_question']
    try:
        response = chat_engine.query(query)
        st.success(f"Question: {query}\n\n\nAnswer: {response}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if col4.button("random question"):
    st.session_state['random_question'] = generator.get_random_question()

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
<p>for questions, write to algorithms.automation[at]gmail by <a  href="https://www.anonnete.net/" target="_blank">denisa kera</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
