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

    # define the function to visualize the selected files
    def visualize_files(selected_files):
        dfs = []
        for file in selected_files:
            contents = st.session_state[file]
            if contents:
                df = pd.read_xml(contents, xpath=".//trkpt")
                dfs.append(df)
        if dfs:
            data = pd.concat(dfs)
            st.dataframe(data)
        else:
            st.write("No files selected.")
    # get access to the uploaded gpx files 
    selected_files = st.session_state.selected_files
    visualize_files(selected_files)

