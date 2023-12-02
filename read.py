import pandas as pd
import streamlit as st
from database import view_data, runquery, make_bill, runquery

def readData(chr):
    StoreData, Wine_BottlesData, StockData, CartData, BillData = view_data()

    if chr=='Store':
        st.subheader("Store Data")
        store_df = pd.DataFrame(StoreData, columns = ["StoreId", "StoreName", "PhoneNumber", "EmailId", "Location", "Landmark", "City", "State"])
        st.dataframe(store_df)

    if chr=='WineBottles':
        st.subheader("Wine Bottle Data")
        Wine_BottlesData_df = pd.DataFrame(Wine_BottlesData, columns = ["WineBottleId", "Name", "MRP", "Type", "Age", "ABV", "Demand"])
        st.dataframe(Wine_BottlesData_df)

    if chr=='Stock':
        st.subheader("Stock Data")
        Stock_df = pd.DataFrame(StockData, columns = ["StoreId", "WineBottleId", "Quantity"])
        st.dataframe(Stock_df)

    if chr=='Cart':
        st.subheader("Cart Data")
        Cart_df = pd.DataFrame(CartData, columns = ["Store_Id","Wine_Bottle_Id","Quantity"])
        st.dataframe(Cart_df)

    if chr=='':
        st.subheader("Store Data")
        store_df = pd.DataFrame(StoreData, columns = ["StoreId", "StoreName", "PhoneNumber", "EmailId", "Location", "Landmark", "City", "State"])
        st.dataframe(store_df)

        st.subheader("Wine Bottle Data")
        Wine_BottlesData_df = pd.DataFrame(Wine_BottlesData, columns = ["WineBottleId", "Name", "MRP", "Type", "Age", "ABV", "Demand"])
        st.dataframe(Wine_BottlesData_df)

        st.subheader("Stock Data")
        Stock_df = pd.DataFrame(StockData, columns = ["StoreId", "WineBottleId", "Quantity"])
        st.dataframe(Stock_df)

        st.subheader("Cart Data")
        Cart_df = pd.DataFrame(CartData, columns = ["Store_Id","Wine_Bottle_Id","Quantity"])
        st.dataframe(Cart_df)

        st.subheader("Bill Data")
        Bill_df = pd.DataFrame(BillData, columns = ["Bill","Created_Time"])
        st.dataframe(Bill_df)

# def bill():
#     z=make_bill()
#     data = {"Total_Cost":[z]}
#     price_df=pd.DataFrame(data,columns=['Total_Cost'])
#     st.dataframe(price_df)


def custom():
    result=runquery("Select m.Man_id, m.Name from Manufacturer m inner join Wine_Bottles wb on m.type=wb.type where wb.wine_bottle_id in (Select wb.wine_bottle_id from wine_bottles wb inner join cart on wb.wine_bottle_id=cart.wine_bottle_id);")
    result_df=pd.DataFrame(result,columns=["Man_id","Man_name"])
    st.dataframe(result_df)