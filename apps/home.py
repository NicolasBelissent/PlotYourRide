import streamlit as st
import leafmap.foliumap as leafmap
import folium
import streamlit as st
import pandas as pd

def app():
    st.title("Home")

    st.markdown(
        """
  """
    )


    # define the function to handle file uploads
    def upload_files():
        uploaded_files = st.file_uploader("Upload GPX files", type=["gpx"], accept_multiple_files=True)
        if uploaded_files:
            # create a checkbox for each uploaded file
            for file in uploaded_files:
                st.session_state[file.name] = st.checkbox(file.name, key=file.name)
            # store selected file names in session state
            selected_files = [file.name for file in uploaded_files if st.session_state.get(file.name)]
            st.session_state.selected_files = selected_files
            return selected_files

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

    # call the upload_files function on the app's home page
    selected_files = upload_files()

    # call the visualize_files function to display the selected files
    visualize_files(selected_files)
