import os
import time
import json
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.utils import styled_print, create_dir, save_uploadedfile, extract_paragraphs, extract_fandom_wikis

raw_data_dir = create_dir("./", "data/raw-data")
out_dir = create_dir("./", "data/processed-data")
config_dir = create_dir("./", "data/config")


# Set the title and instructions for the page
styled_print("Initiating Data Extractor", header=True)

st.set_page_config(
    page_title="Data Extractor",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/viralbthakar/',
        'Report a bug': "https://github.com/viralbthakar/fire-and-blood-qa/issues/new/choose",
        'About': "This is an *extremely* cool app!"
    }
)

st.title("Data Extractor Tool")
st.write("Tool to extract data from different sources.")

st.header(":closed_book: Extract Paragraphs from Book")
# Create a file upload component and set its type to CSV
docx_file_uploader = st.file_uploader("Upload a DOCX file", type=["docx"])

# If a file is uploaded
if docx_file_uploader is not None:
    book_docx_path = save_uploadedfile(docx_file_uploader, path=raw_data_dir)
    st.success(f"Saved File: {book_docx_path}")

    start_book_extraction = st.button("Extract Paragraphs!")
    if start_book_extraction:
        with st.spinner('Extracting Paragraphs...'):
            book_text_dir = create_dir(out_dir, "clean-csvs")
            row_paragraphs = extract_paragraphs(
                book_docx_path, min_char_count=10)
            styled_print(
                f"Found Total {len(row_paragraphs)} Paragraphs from the Book {book_docx_path}", header=True)
            book_df = pd.DataFrame(row_paragraphs.items(),
                                   columns=["id", "paragraphs"])
            book_df.to_csv(os.path.join(
                book_text_dir, "book-raw-paragraphs.csv"), index=False, header=True)
            st.success(
                f"Found Total {len(row_paragraphs)} Paragraphs from the Book {book_docx_path}")
            st.subheader("Sample Paragraphs")
            st.dataframe(book_df)


st.header(":movie_camera: Extract Wikis from Fandom!")
config_file_uploader = st.file_uploader("Upload a CONFIG file", type=["json"])
if config_file_uploader is not None:
    config_file = save_uploadedfile(config_file_uploader, path=config_dir)
    st.success(f"Saved File: {config_file}")
    styled_print(
        "Extracting Data for House of Dragons Season", header=True)

    start_hod_extraction = st.button("Extract Wikis!")
    if start_hod_extraction:
        with st.spinner('Extracting Wikis...'):
            hod_out_dir = create_dir(out_dir, "house-of-dragons", header=False)

            with open(config_file, 'r') as f:
                hod_data = json.load(f)

            for key in hod_data["house-of-dragons"].keys():
                st.subheader(f"{key.capitalize()} of House of Dragons")
                styled_print(
                    f"Working on {key} of House of Dragons", header=True)
                element_dir = create_dir(hod_out_dir, key, header=False)
                elements = {epi["title"]: epi["url"] for epi in
                            hod_data["house-of-dragons"][key]}
                if key != 'subtitles':
                    headers = {epi["title"]: epi["headers"]
                               for epi in hod_data["house-of-dragons"][key]}

                styled_print(
                    f"Found {len(elements.keys())} {key} ...", header=True)
                for title, url in elements.items():
                    st.subheader(f"{title}")
                    styled_print(f"Extracting {title} {key} ...")
                    text_dict = extract_fandom_wikis(url, headers[title])
                    styled_print(
                        f"Writing Text into {title.replace(' ', '-')}.csv ...")
                    hod_df = pd.DataFrame.from_dict(text_dict)
                    hod_df.to_csv(os.path.join(
                        element_dir, f"{title.replace(' ', '-')}.csv"), index=False, header=False)
                    st.subheader("Sample Data")
                    st.dataframe(hod_df)

data_cleaner_page = st.button("Data Cleaner!")
if data_cleaner_page:
    switch_page("Data Cleaner")
