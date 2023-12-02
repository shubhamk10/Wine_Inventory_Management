import streamlit as st
from Admin_database import create_tables
from Admin_create import createTablesfromXML
from Admin_read import readData, custom
# from update import updateEntry
# from delete import deleteEntry


def Admin_main():
    create_tables()
    st.title("Wine_ManagementSystem")
    menu = ["Add", "View", "Most Storage Capacity","Custom Query"]
    choice = st.sidebar.selectbox("Views", menu)
    if choice == "Add":
        st.subheader("Upload XML File")
        createTablesfromXML()

    if (choice == "View"):
        option = st.selectbox('Select table to view', ('Customer', 'Store', 'WineBottles', 'Retailer','Manufacturer','Cellar','Stock'))
        readData(option)

    # if choice == "ViewAll":
    #     st.subheader("View all tables")
    #     readData('')

    if choice == "Most Storage Capacity":
        q="SELECT Man_id, Name AS Manufacturer_Name ,Type from Manufacturer where Man_id in (Select Manufacturer.Man_id from Cellar INNER JOIN Manufacturer ON Cellar.Man_id=Manufacturer.Man_id where Quantity>5000 ORDER BY Quantity DESC) limit 3 "
        custom(q)
    # elif choice == "Update":
    #     st.subheader("Update")
    #     updateEntry()

    # elif choice == "Delete":
    #     st.subheader("Delete")
    #     deleteEntry()
    if choice == "Custom Query":
        st.text('Enter the query in the box below')
        q = st.text_input('Enter query')
        if (st.button('Run')):
            custom(q)

if __name__ == "__main__":
    Admin_main()
