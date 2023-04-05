import os
import glob
import pandas as pd
import streamlit as st
from src.paragraph_cleaner import ParagraphCleaner
from streamlit_extras.switch_page_button import switch_page
from src.utils import styled_print, create_dir, fetch_session_state, add_to_session_state

# Set the title and instructions for the page
styled_print("Initiating Data Analyzer", header=True)

st.set_page_config(
    page_title="Data Analyzer",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/viralbthakar/',
        'Report a bug': "https://github.com/viralbthakar/fire-and-blood-qa/issues/new/choose",
        'About': "This is an *extremely* cool app!"
    }
)

clean_data_dir = fetch_session_state(st.session_state, "clean-csvs")

st.title("Data Analysis Tool")
st.write("Tool to perform data analysis on clean data.")
