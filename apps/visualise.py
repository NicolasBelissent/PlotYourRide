import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from io import BytesIO
import altair as alt
import json
import folium
from gpxplotter import create_folium_map, read_gpx_file, add_segment_to_map
import gpxplotter
import numpy as np
from altair_saver import save
import pandas as pd
import pdfkit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import gpxpy
import os

def download_map_pdf(map_html):
    # Set up Selenium
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Create a temporary HTML file containing the map
    tmp_map_file = "tmp_map.html"
    with open(tmp_map_file, "w") as f:
        f.write(map_html)

    # Wait for the map to fully render
    time.sleep(5)

    # Use pdfkit to create a PDF of the map
    pdf_file_name = "map.pdf"
    pdfkit.from_file(tmp_map_file, pdf_file_name)

    # Close the Selenium driver and delete the temporary files
    driver.quit()
    os.remove(tmp_map_file)

    # Download the PDF file
    with open(pdf_file_name, "rb") as f:
        pdf_bytes = f.read()
        st.download_button(
            label="Download Map PDF",
            data=pdf_bytes,
            file_name=pdf_file_name,
            mime="application/pdf"
        )
    os.remove(pdf_file_name)

def combine_gpx_files(gpx_files):
    combined_gpx = gpxpy.gpx.GPX()

    for gpx_file in gpx_files:
        #gpx = gpxpy.parse(gpx_file)
        for track in gpx_file.tracks:
            combined_gpx.tracks.append(track)
    
    combined_xml = combined_gpx.to_xml()
    file_name = "combined.gpx"
    with open(file_name, "w") as f:
        f.write(combined_xml)
    
    return combined_xml

# def combine_gpx_files(files):
#     # Create a new GPX file
#     combined_gpx = ET.Element("gpx", xmlns="http://www.topografix.com/GPX/1/1")

#     # Iterate over all the input GPX files
#     for file in files:
#         # Parse the GPX file
#         tree = ET.parse(file)
#         root = tree.getroot()

#         # Iterate over all the waypoints, tracks, and routes in the GPX file
#         for element in root:
#             if element.tag == "wpt":
#                 # Add the waypoint to the combined GPX file
#                 combined_gpx.append(element)
#             elif element.tag == "trk":
#                 # Iterate over all the track segments in the track
#                 for segment in element:
#                     # Add the track segment to the combined GPX file
#                     combined_gpx.append(segment)
#             elif element.tag == "rte":
#                 # Add the route to the combined GPX file
#                 combined_gpx.append(element)

#     # Create a file-like object in memory to write the GPX file to
#     output = BytesIO()
#     ET.ElementTree(combined_gpx).write(output, encoding="UTF-8", xml_declaration=True)
#     output.seek(0)

#     # Return the file-like object
#     return output

def visualise_gpx(the_map, filename, segment_name = 'Bike Ride', tile = 'stamenterrain'):
    st.write(type(filename))
    for track in filename.tracks:
        for _, segment in enumerate(track['segments']):
            add_segment_to_map(the_map, segment,
                            cmap='viridis', line_options={'weight': 8})

    # Create a chart using Altair
    idx = len(segment['elevation'])

    data = {
        'x': segment['Distance / km'],
        'y': segment['elevation'],
    }
    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Specify the data type for the x encoding field
    line = alt.Chart(df).mark_line().encode(
        x=alt.X('x', title='Distance / km'),
        y=alt.Y('y', title='Elevation / m')
    )

    WIDTH = 400
    HEIGHT = 200

    line = line.properties(
        width=WIDTH,
        height=HEIGHT
    )

    # Save the chart as a PNG image
    #png_bytes = save(line, format='png')
    line.save('test.html')
    # Encode the PNG image as base64 string
    chart_html = open("test.html", "r").read()
    # Create the HTML content for the popup
    html = ''' <h1 style="font-family: Verdana"> {0}</h1><br>
            <p style="font-family: Verdana"> Distance: {1} </p>
            <p style="font-family: Verdana"> Total elevation Gain: {2} </p>
            <p style="font-family: Verdana"> Average Speed: {3} </p>
            <img src="data:image/png;base64,{4}" />

            <br>
            {4}
            '''.format(segment_name,str(np.round(segment['distance'][-1]/1000,2))+' km', str(np.round(segment['elevation-up'], 1)) +' m', str(np.round(np.mean(segment['Velocity / km/h']), 1)) + ' km/h', chart_html)

    iframe = folium.IFrame(html=html, width=500, height=500)
    popup = folium.Popup(iframe, width=500, height=500)

    folium.TileLayer(tile).add_to(the_map)

    marker = folium.Marker(
        location=segment['latlon'][idx],
        popup=popup,
        icon=folium.Icon(icon='star'),
    )
    marker.add_to(the_map)

















# Create a Streamlit app that allows the user to upload GPX files and download the combined file
def app():
    st.title("Visualise your Ride")

    # Allow the user to upload multiple GPX files
    uploaded_files = st.file_uploader("Upload GPX files", type="gpx", accept_multiple_files=True)

    # If the user has uploaded files, combine them into a single file and allow the user to download it
    if uploaded_files:
        # Combine the GPX files into a single file
        gpx_files = [gpxpy.parse(file) for file in uploaded_files]

        col1, col2, col3, col4 = st.columns([1,1,1,1])

        with col1:
            combined_file = combine_gpx_files(gpx_files)

            st.download_button(
            label="Download Combined GPX File",
            data=combined_file,
            file_name="combined.gpx",
            mime="application/gpx+xml")

        with col2:
            # Add the other two buttons to the row
            if st.button("Visualise your Trip"):
                folium_map = create_folium_map()
                # Loop through each uploaded file and visualize it
                for gpx_file in gpx_files:
                    if gpx_file is not None:
                        
                        # Read the contents of the file
                        gpx_data = read_gpx_file(gpx_file)
                        st.code(gpx_data)
                        st.code(type(gpx_data))

                        # Pass the file contents through the visualise_gpx() function
                        visualise_gpx(folium_map,list(gpx_data))
        with col3:
            # Add a button to download a PDF of the map
            if st.button("Get Trip Statistics"):
                st.text('...')

        with col4:

            if st.button("Download Map PDF"):

                try:
                    map_html = folium_map._repr_html_()
                    download_map_pdf(map_html)
                except NameError:
                    st.text('Please visualise before downloading PDF')
