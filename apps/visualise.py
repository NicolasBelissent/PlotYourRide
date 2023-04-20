import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
from upload_files import upload_file




def app():

    st.title("Visualise your Ride")

    st.markdown(
        """
        More dev work to come
    """
    )


    selected_files = upload_file()

    if selected_files:
        st.write("Selected files:")
        for name, file in selected_files.items():
            st.write(name)

