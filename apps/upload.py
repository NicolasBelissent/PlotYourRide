import streamlit as st

# create an empty list to hold the uploaded file data
uploaded_files = []

# define the function to handle file uploads
def upload_file():
    files = st.file_uploader("Upload GPX files", type=["gpx"], accept_multiple_files=True)
    if files:
        for file in files:
            uploaded_files.append(file)
        st.success(f"{len(files)} file(s) uploaded successfully.")

# call the upload_file function on the app's home page
upload_file()

# display a link to the uploaded file(s) on all pages
if uploaded_files:
    st.sidebar.header("Uploaded Files")
    for file in uploaded_files:
        st.sidebar.markdown(f"[{file.name}]({file.url})", unsafe_allow_html=True)
