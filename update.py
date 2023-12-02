import streamlit as st
import pandas as pd
from database import update_cart


def addCart(store,bottle,quantity):

    y=update_cart(store,bottle,quantity)
    if y==1:
        st.subheader("Successful")
    else:
        st.subheader("Insufficient Quantity")

def delcart(store,bottle,quantity):

    qty=-quantity
    y=update_cart(store,bottle,qty)
    if y==1:
        st.subheader("Successful")
    else:
        st.subheader("Not enough quantity present in Cart")
