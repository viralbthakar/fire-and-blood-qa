import os
import time
import pandas as pd
import streamlit as st
from src.utils import styled_print, create_dir, save_uploadedfile, extract_paragraphs

raw_data_dir = create_dir("./", "data/raw-data")
out_dir = create_dir("./", "data/processed-data")

st.set_page_config(page_title="Data Extractor")

# Set the title and instructions for the page
st.title("Data Extractor Tool")
st.write("Tool to extract data from different sources.")

# Create a file upload component and set its type to CSV
docx_file = st.file_uploader("Upload a DOCX file", type=["docx"])

# If a file is uploaded
if docx_file is not None:
    book_docx_path = save_uploadedfile(docx_file, path=raw_data_dir)
    st.success(f"Saved File: {book_docx_path}")

    styled_print("Initiating Data Creator", header=True)

    start_extraction = st.button("Extract!")
    if start_extraction:
        with st.spinner('Extracting Paragraphs...'):
            book_text_dir = create_dir(out_dir, "clean-csvs")
            row_paragraphs = extract_paragraphs(
                book_docx_path, min_char_count=1)
            styled_print(
                f"Found Total {len(row_paragraphs)} Paragraphs from the Book {book_docx_path}", header=True)
            book_df = pd.DataFrame(row_paragraphs.items(),
                                   columns=["id", "paragraphs"])
            book_df.to_csv(os.path.join(
                book_text_dir, "book-raw-paragraphs.csv"), index=False, header=True)
            st.dataframe(book_df)
