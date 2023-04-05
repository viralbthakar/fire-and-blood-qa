import os
import glob
import streamlit as st
import pandas as pd
from src.utils import styled_print, create_dir, fetch_session_state, add_to_session_state


out_dir = fetch_session_state(st.session_state, "out_dir")

csv_files = []
for root, dirs, files in os.walk(out_dir):
    for file in files:
        if (file.endswith(".csv")):
            csv_files.append(os.path.join(root, file))
csv_files.append("All Files")


st.header("Data Cleaning Workflow")
selected_files = st.multiselect("Select Files", csv_files, None)
if "All Files" in selected_files:
    selected_files = [f for f in csv_files]

load_files = st.button("Load CSVs!")
if load_files:
    cols = []
    for f in selected_files:
        st.success(f"Found {f} File for Cleaning")
        data_df = pd.read_csv(f)
        cols.extend(list(data_df.columns))
    cols = list(set(cols))

cols_to_merge = st.multiselect(
    'Select Columns to Merge Dataframes', cols, None)
st.write('You selected:', cols_to_merge)
