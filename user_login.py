import streamlit as st
import mysql.connector as myconn
import pandas as pd


def fetch_mail(email,password):
    mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM user_info")
    columns = ["User_id", "Name","Mobile","Address","Emails","Password"]
    data = cursor.fetchall()
    
    # Convert data to DataFrame
    data = pd.DataFrame(data, columns=columns)
    email_data=data[data["Emails"]==email]
    if not email_data.empty:  # Check if the filtered DataFrame is not empty
        if email_data["Password"].iloc[0] == password:  # Use .iloc[0] to access the first row
            return True
        
    
    return False 

    cursor.close()
    mydb.close()

st.title("Sign In")
email = st.text_input("Enter your email:")
password = st.text_input("Enter your password:", type="password")

# Add a login button
if st.button("Login"):
    if email and password:
        if fetch_mail(email,password):
            st.write(f"Logging in with Email: {email}") 
            st.switch_page("pages/app_user.py")
        else:
            st.write("Wrong Email or Password!!")
            
    else:
        st.warning("Please enter both email and password")

b1=st.button("Sign-Up")

if b1:
    st.switch_page("pages/Signup.py")
