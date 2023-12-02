import streamlit as st
from Admin_database import add_data

def createTablesfromXML():
    uploaded_file = st.file_uploader("Upload an XML file", type=["xml"])

    if uploaded_file is not None:
        add_data(uploaded_file)
        st.success("Data imported from the XML file and inserted into the database.")
