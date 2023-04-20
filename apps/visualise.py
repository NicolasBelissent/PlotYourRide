import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
from upload import upload_files




def app():

    st.title("Visualise your Ride")

    st.markdown(
        """
        More dev work to come
    """
    )


    selected_files = upload_files()

    if selected_files:
        st.write("Selected files:")
        for name, file in selected_files.items():
            st.write(name)

