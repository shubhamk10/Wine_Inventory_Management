import streamlit as st
from database import add_data

def createTablesfromXML():
    default_file_path = "C:\Gouda\Sem-5\DBMS\DBMS Miniproject\Wine_Shop.xml"
    uploaded_file = open(default_file_path, 'rb')
    if uploaded_file is not None:
        add_data(uploaded_file)
        st.success("Data imported from the XML file and inserted into the database.")
