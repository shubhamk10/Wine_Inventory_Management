import pandas as pd
import streamlit as st
from Admin_database import view_data, runquery

def readData(chr):
    StoreData, CustomerData, Wine_BottlesData, StockData, RetailerData, ManufacturerData, CellarData = view_data()

    if chr=='Store':
        st.subheader("Store Data")
        store_df = pd.DataFrame(StoreData, columns = ["StoreId", "StoreName", "PhoneNumber", "EmailId", "Location", "Landmark", "City", "State"])
        st.dataframe(store_df)

    if chr=='Customer':
        st.subheader("Customer Data")
        Customer_df = pd.DataFrame(CustomerData, columns = ["StoreId", "Name", "CustId", "Status", "PhoneNumber"])
        st.dataframe(Customer_df)

    if chr=='WineBottles':
        st.subheader("Wine Bottle Data")
        Wine_BottlesData_df = pd.DataFrame(Wine_BottlesData, columns = ["WineBottleId", "Name", "MRP", "Type", "Age", "ABV", "Demand"])
        st.dataframe(Wine_BottlesData_df)

    if chr=='Stock':
        st.subheader("Stock Data")
        Stock_df = pd.DataFrame(StockData, columns = ["StoreId", "WineBottleId", "Quantity", "RetailerId"])
        st.dataframe(Stock_df)

    if chr=='Retailer':
        st.subheader("Retailer Data")
        Retailer_df = pd.DataFrame(RetailerData, columns = ["RetailerId", "Name", "WineBottleId", "RSellingPrice"])
        st.dataframe(Retailer_df)

    if chr=='Manufacturer':
        st.subheader("Manufacturer Data")
        Manufacturer_df = pd.DataFrame(ManufacturerData, columns = ["ManId", "Name", "Type", "Capacity", "ManufacturerSellingPrice", "PhoneNumber", "Location"])
        st.dataframe(Manufacturer_df)

    if chr=='Cellar':
        st.subheader("Cellar Data")
        Cellar_df = pd.DataFrame(CellarData, columns = ["ManId", "CellarId", "Name", "Quantity"])
        st.dataframe(Cellar_df)

    if chr=='':
        st.subheader("Store Data")
        store_df = pd.DataFrame(StoreData, columns = ["StoreId", "StoreName", "PhoneNumber", "EmailId", "Location", "Landmark", "City", "State"])
        st.dataframe(store_df)

        st.subheader("Customer Data")
        Customer_df = pd.DataFrame(CustomerData, columns = ["StoreId", "Name", "CustId", "Status", "PhoneNumber"])
        st.dataframe(Customer_df)

        st.subheader("Wine Bottle Data")
        Wine_BottlesData_df = pd.DataFrame(Wine_BottlesData, columns = ["WineBottleId", "Name", "MRP", "Type", "Age", "ABV", "Demand"])
        st.dataframe(Wine_BottlesData_df)

        st.subheader("Stock Data")
        Stock_df = pd.DataFrame(StockData, columns = ["StoreId", "WineBottleId", "Quantity", "RetailerId"])
        st.dataframe(Stock_df)

        st.subheader("Retailer Data")
        Retailer_df = pd.DataFrame(RetailerData, columns = ["RetailerId", "Name", "WineBottleId", "RSellingPrice"])
        st.dataframe(Retailer_df)

        st.subheader("Manufacturer Data")
        Manufacturer_df = pd.DataFrame(ManufacturerData, columns = ["ManId", "Name", "Type", "Capacity", "ManufacturerSellingPrice", "PhoneNumber", "Location"])
        st.dataframe(Manufacturer_df)

        st.subheader("Cellar Data")
        Cellar_df = pd.DataFrame(CellarData, columns = ["ManId", "CellarId", "Name", "Quantity"])
        st.dataframe(Cellar_df)

def custom(command):
    x=command.split()
    for i in range(0,len(command)):
        if command[i]=='*':
            result=runquery(command)
            result_df=pd.DataFrame(result)
            st.dataframe(result_df)
        if command[i:i+4]=='from' or command[i:i+4]=="FROM":
            y=i
            z=command[len(x[0])+1:y-1]
            z=z.split(',')
            result=runquery(command)
            for i in range(len(z)):
                if 'as' in z[i] or 'AS' in z[i]:
                    zz=z[i].split()
                    z[i]=zz[2]
                    result_df=pd.DataFrame(result, columns=z)
            break
        st.dataframe(result_df)