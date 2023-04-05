import os
import glob
import pandas as pd
import streamlit as st
from src.paragraph_cleaner import ParagraphCleaner
from streamlit_extras.switch_page_button import switch_page
from src.utils import styled_print, create_dir, fetch_session_state, add_to_session_state

# Set the title and instructions for the page
styled_print("Initiating Data Cleaner", header=True)

st.set_page_config(
    page_title="Data Cleaner",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/viralbthakar/',
        'Report a bug': "https://github.com/viralbthakar/fire-and-blood-qa/issues/new/choose",
        'About': "This is an *extremely* cool app!"
    }
)

out_dir = fetch_session_state(st.session_state, "out_dir")
clean_data_dir = create_dir(out_dir, "clean-csvs")
st.session_state = add_to_session_state(
    st.session_state, "clean_data_dir", clean_data_dir)

st.title("Data Cleaning Tool")
st.write("Tool to clean data from different sources.")

csv_files = []
for root, dirs, files in os.walk(out_dir):
    for file in files:
        if (file.endswith(".csv")):
            csv_files.append(os.path.join(root, file))

st.header("Data Cleaning Workflow")
selected_files = st.selectbox("Select Files", csv_files)
selected_files = [selected_files]

debug_data_clean = st.button("Debug Clean!")
all_data_clean = st.button("Clean All!")

if debug_data_clean:
    for i, file in enumerate(selected_files):
        data_dict = pd.read_csv(file)
        st.subheader(f"Raw Data From {file}")
        st.dataframe(data_dict)
        cleaner = ParagraphCleaner(
            data_dict, 'paragraphs', 'cleaned_paragraphs')
        with st.spinner('Wait for it...'):
            data_dict = cleaner.clean_data()
        st.subheader(f"Clean Data From {file}")
        st.dataframe(data_dict)

if all_data_clean:
    selected_files = [f for f in csv_files]
    with st.spinner('Cleaning all data ...'):
        for i, file in enumerate(selected_files):
            data_dict = pd.read_csv(file)
            cleaner = ParagraphCleaner(
                data_dict, 'paragraphs', 'cleaned_paragraphs')
            data_dict = cleaner.clean_data()
            clean_file_path = os.path.join(
                clean_data_dir, f"{os.path.basename(file)}")
            data_dict.to_csv(clean_file_path, index=False, header=True)
            st.success(f"Saved File: {clean_file_path}")

st.sidebar.success("Data Cleaning Done!")

data_analysis_page = st.button("Data Analyzer!")
if data_analysis_page:
    switch_page("Data Analysis")
    print(st.session_state)
