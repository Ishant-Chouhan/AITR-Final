import streamlit as st
import mysql.connector as myconn
import pandas as pd
def user_id_generate():
    mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
    cursor = mydb.cursor()
    
    cursor.execute("SELECT max(User_id) FROM user_info")
    columns = ["User_id"]
    data = cursor.fetchall()
    
    # Convert data to DataFrame
    data = pd.DataFrame(data, columns=columns)
    return  data
st.title("Sign Up")
d=user_id_generate()

user_id = int(d.iloc[0,0])+1 
name = st.text_input("Enter your name:")
mobile = st.text_input("Enter your Mobile number:")
street = st.text_input("Enter Name of the Street:")
city = st.text_input("Enter city:")
state = st.text_input("Enter state:")
pincode = st.text_input("Enter pincode:")

# Construct Address safely
Address = f"{street}, {city}, {state} - {pincode}".strip()

# 🔹 Email field is prefilled from the login page
email = st.text_input("Enter your email:")  

password = st.text_input("Create a password:", type="password")

def dump_into_user(user_id, name, mobile, Address, email, password):
    try:
        mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
        cursor = mydb.cursor()


        sql = """INSERT INTO user_info (User_id, Name, Mobile, Address, email, password)
                 VALUES (%s, %s, %s, %s, %s, %s)"""

        values = (user_id, name, mobile, Address, email, password)
        cursor.execute(sql, values)
        mydb.commit()

        return True

    except myconn.Error as err:
        st.error(f"Database error: {err}")
        return False

    finally:
        cursor.close()
        mydb.close()

if st.button("Register"):
    if all([name, mobile, street, city, state, pincode, email, password]):  # Ensure no empty fields
        if dump_into_user(user_id, name, mobile, Address, email, password):
            st.success("Account created successfully! 🎉")
            
        else:
            st.warning("Account not created due to a technical issue! ❌")
    else:
        st.warning("Please fill in all fields! ⚠️")
