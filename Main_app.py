import streamlit as st
from app import *
from Admin_app import *

# from update import updateEntry
# from delete import deleteEntry

# def signup():
#     st.subheader("Sign Up")
#     new_username = st.text_input("Username")
#     new_password = st.text_input("Password", type='password')
    
#     if st.button("Sign Up"):
#         if new_username and new_password:
#             if new_username not in user_credentials:
#                 user_credentials[new_username] = {'password': new_password}
#                 st.success("Sign up successful! You can now log in.")
#             else:
#                 st.warning("Username already exists. Please choose a different one.")
#         else:
#             st.warning("Username and password cannot be empty.")

# def login():
#     st.subheader("Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type='password')
    
#     if st.button("Login"):
#         if username and password:
#             if username in user_credentials and user_credentials[username]['password'] == password:
#                 st.success(f"Welcome, {username}!")
#                 # Add your application logic after successful login
#             else:
#                 st.warning("Invalid username or password. Please try again.")
#         else:
#             st.warning("Username and password cannot be empty.")

# def change_password(username):
#     st.subheader("Change Password")
#     old_password = st.text_input("Old Password", type='password')
#     new_password = st.text_input("New Password", type='password')
    
#     if st.button("Change Password"):
#         if old_password and new_password:
#             if user_credentials.get(username, {}).get('password') == old_password:
#                 user_credentials[username]['password'] = new_password
#                 st.success("Password changed successfully!")
#             else:
#                 st.warning("Old password is incorrect. Please try again.")
#         else:
#             st.warning("Old and new passwords cannot be empty.")

def main():
    menu = ["Admin","Customer"]
    choice = st.sidebar.selectbox("Role", menu)
    if choice=="Admin":
        Admin_main()
    if choice=="Customer":
        customer_main()
if __name__ == "__main__":
    main()
