import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd




def app():

    st.title("Visualise your Ride")

    st.markdown(
        """
        More dev work to come
    """
    )

    # define the function to handle file uploads
    def upload_file():
        uploaded_files = st.file_uploader("Upload GPX files", type=["gpx"], accept_multiple_files=True)
        if uploaded_files:
            # create a dictionary of file names and their respective file paths
            selected_files = {}
            for file in uploaded_files:
                if st.checkbox(file.name):
                    file_contents = file.read()
                    selected_files[file.name] = file_contents
            return selected_files

    # create the Streamlit app
    def app():
        # set the app title and instructions
        st.title("GPX File Visualization")
        st.write("Upload GPX files and select which files to use for visualization.")

        # call the upload_file function to handle file uploads
        selected_files = upload_file()
        if selected_files:
            st.write(f"You have selected {len(selected_files)} files for visualization.")
            st.write(selected_files)

