import os
import glob
import streamlit as st
import pandas as pd
from src.utils import styled_print, create_dir

# out_dir = create_dir("./", "data/processed-data")
files = glob.glob(os.path.join(out_dir, "*.csv"))
files.append("All Files")

selected_file = st.selectbox("Select File", files)
st.write(selected_file)
