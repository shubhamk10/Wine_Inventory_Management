import streamlit as st
from database import create_tables, delete_data, exists_database, procedures, triggers
from create import createTablesfromXML
from read import readData, custom
from update import addCart, delcart
# from update import updateEntry
# from delete import deleteEntry

def customer_main():
    create_tables()
    procedures()
    triggers()
    st.title("Wine_Shop")
    menu = ["Initialize","View","Order","Custom Query"]
    choice = st.sidebar.selectbox("Views", menu)
    #createTablesfromXML()
    if choice=="Initialize":
        if exists_database():
            delete_data()
        createTablesfromXML()

    if (choice == "View"):
        option = st.selectbox('Select table to view', ('Store', 'WineBottles','Stock','Cart'))
        readData(option)

    if choice == "Order":
        st.subheader("Choices")
        readData('')
        store = st.selectbox('Select Store',(1,2,3,4,5))
        bottle = st.selectbox('Select Bottle',(1,2,3,4,5))
        qty = st.selectbox('Select Quantity',(1,2,3,4,5))
        if (st.button('Add')):
           addCart(store,bottle,qty)
        if (st.button('Delete')):
            delcart(store,bottle,qty)
    
    # if choice=="Generate Bill":
    #     st.subheader("Bill")
    #     bill()




    # elif choice == "Update":
    #     st.subheader("Update")
    #     updateEntry()

    # elif choice == "Delete":
    #     st.subheader("Delete")
    #     deleteEntry()
    if choice == "Custom Query":
        custom()

if __name__ == "__main__":
    customer_main()
