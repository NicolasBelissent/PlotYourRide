import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd


# # define the function to handle file uploads
# def upload_file():
#     uploaded_files = st.file_uploader("Upload GPX files", type=["gpx"], accept_multiple_files=True)
#     if uploaded_files:
#         # create a dictionary of file names and their respective file paths
#         selected_files = {}
#         for file in uploaded_files:
#             if st.checkbox(file.name):
#                 file_contents = file.read()
#                 selected_files[file.name] = file_contents
#         return selected_files

# def app():

#     st.title("Visualise your Ride")

#     # set the app instructions
#     st.write("Upload GPX files and select which files to use for visualization.")

#     # call the upload_file function to handle file uploads
#     selected_files = upload_file()
#     if selected_files:
#         st.write(f"You have selected {len(selected_files)} files for visualization.")
#         st.write(selected_files)

import streamlit as st
import xml.etree.ElementTree as ET
from io import BytesIO

def combine_gpx_files(files):
    # Create a new GPX file
    combined_gpx = ET.Element("gpx", xmlns="http://www.topografix.com/GPX/1/1")

    # Iterate over all the input GPX files
    for file in files:
        # Parse the GPX file
        tree = ET.parse(file)
        root = tree.getroot()

        # Iterate over all the waypoints, tracks, and routes in the GPX file
        for element in root:
            if element.tag == "wpt":
                # Add the waypoint to the combined GPX file
                combined_gpx.append(element)
            elif element.tag == "trk":
                # Iterate over all the track segments in the track
                for segment in element:
                    # Add the track segment to the combined GPX file
                    combined_gpx.append(segment)
            elif element.tag == "rte":
                # Add the route to the combined GPX file
                combined_gpx.append(element)

    # Create a file-like object in memory to write the GPX file to
    output = BytesIO()
    ET.ElementTree(combined_gpx).write(output, encoding="UTF-8", xml_declaration=True)
    output.seek(0)

    # Return the file-like object
    return output

# Create a Streamlit app that allows the user to upload GPX files and download the combined file
def app():
    st.title("Visualise your Ride")

    # Allow the user to upload multiple GPX files
    uploaded_files = st.file_uploader("Upload GPX files", type="gpx", accept_multiple_files=True)

    # If the user has uploaded files, combine them into a single file and allow the user to download it
    if uploaded_files:
        # Combine the GPX files into a single file
        combined_file = combine_gpx_files(uploaded_files)

        # Display a download button that allows the user to download the combined file
        st.download_button(
            label="Download Combined GPX File",
            data=combined_file.getvalue(),
            file_name="combined.gpx",
            mime="application/gpx+xml"
        )
