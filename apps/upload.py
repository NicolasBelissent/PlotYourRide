import os
import geopandas as gpd
import streamlit as st

# create an empty list to hold the uploaded file data
uploaded_files = []

# define the function to handle file uploads
def upload_file():
    file = st.file_uploader("Upload GPX file", type=["gpx"])
    if file is not None:
        uploaded_files.append(file)
        st.success("File uploaded successfully.")

# call the upload_file function on the app's home page
upload_file()

# display a link to the uploaded file(s) on all pages
if uploaded_files:
    st.sidebar.header("Uploaded Files")
    for file in uploaded_files:
        st.sidebar.markdown(f"[{file.name}]({file.url})", unsafe_allow_html=True)