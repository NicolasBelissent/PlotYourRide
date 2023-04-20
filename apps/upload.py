import streamlit as st

def app():

    st.title("Upload your GPX files")

    st.markdown(
        """
        More dev work to come
    """
        )
    # create an empty list to hold the uploaded file data
    uploaded_files = []

    # define the function to handle file uploads
    def upload_file():
        files = st.file_uploader("Upload GPX files", type=["gpx"], accept_multiple_files=True)
        if files:
            for file in files:
                uploaded_files.append(file)
            st.success(f"{len(files)} file(s) uploaded successfully.")

