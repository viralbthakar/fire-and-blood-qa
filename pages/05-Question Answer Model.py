import os
import glob
import pandas as pd
import streamlit as st
from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
from streamlit_extras.switch_page_button import switch_page
from src.utils import styled_print, create_dir, fetch_session_state, add_to_session_state, extract_NER, create_qa_pairs_from_NER

# Set the title and instructions for the page
styled_print("Initiating Question Answer Model", header=True)

st.set_page_config(
    page_title="QA Model",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/viralbthakar/',
        'Report a bug': "https://github.com/viralbthakar/fire-and-blood-qa/issues/new/choose",
        'About': "This is an *extremely* cool app!"
    }
)

st.title("Question Answer Model Creation Tool")
st.write("Tool to create question, answer model")
