import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV File Upload")

# Set the title and instructions for the page
st.title("CSV File Upload")
st.write("Please upload a CSV file and wait for the table to be displayed.")

# Create a file upload component and set its type to CSV
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

# If a file is uploaded
if csv_file is not None:
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file)

    # Display the DataFrame as a table
    st.write(df)
