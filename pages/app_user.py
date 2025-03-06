import streamlit as st
import mysql.connector as myconn
import pandas as pd
st.title("Complaint File")
user_id=st.text_input("Enter your user_id:")
complaint_des=st.text_input("Describe about the issue:")

import streamlit as st
import mysql.connector as myconn
import pandas as pd

import smtplib
server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
def send_mail(sender,sender_pass,reciever,message):
    server.login(sender,sender_pass)
    server.sendmail(sender,reciever,message)
    print("mail sent successfully")

def complaint_number():
    mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
    cursor = mydb.cursor()
    
    cursor.execute("SELECT max(complaint_id) FROM complaints")
    result = cursor.fetchone()  # Fetch single row
    
    cursor.close()
    mydb.close()
    
    if result[0] is not None:
        return int(result[0])  # Convert to integer
    else:
        return 0  # If no complaints exist, start from 0


complaint=complaint_number()+1

from answer2 import chat

context=""""{complaint_des}" there was a bus driver driving rushly" give priority for the department to perform execution on it  like is it an emergency, moderate or less priority"""
M=chat(context)
temp1=["Emergency","Moderate","Less Priority"]
for i in temp1:
    if i in M:
        break
priority=i

dep=['Police Department','Cyber Crime Department','Women Helpline','Fire Department','Consumer Protection Department','Child Welfare Department','Traffic Police Department','Social Welfare Department','Disaster Management','Anti-Corruption Bureau','Human Right Department','Muncipal Coporation Department']
context=f"""give answer in a single word, i am giving you a complent that is "{complaint_des}" filed by an indian citizen you have to give the name  from the list of department i am providing to you that is ['Police Department','Cyber Crime Department','Women Helpline','Fire Department','Consumer Protection Department','Child Welfare Department','Traffic Police Department','Social Welfare Department','Disaster Management','Anti-Corruption Bureau','Human Right Department','Muncipal Coporation Department'], use the whole name as mentioned the list"""
D=chat(context)
for i in dep:
    if i in D:
        depart=i
        department_id=dep.index(i)+1
        break
status="In Progress"

sql="""
INSERT INTO complaints (user_id,complaint_id,complaint,priority,department_id,status) 
VALUES (%s, %s, %s, %s, %s, %s)
"""
def show(user_id,complaint,complaint_des,priority,department_id,status):
    st.write(f"Reference_id  - {user_id}")
    st.write(f"Complaint_id  - {complaint}")
    st.write(f"Complaint     - {complaint_des}")
    st.write(f"Priority      - {priority}")
    st.write(f"Department_id - {department_id}")
    st.write(f"Status        - {status}")
    st.markdown(f"Department    - {depart}")

def dump(user_id,complaint,complaint_des,priority,department_id,status):
    data=(user_id,complaint,complaint_des,priority,department_id,status)
    mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
    cursor = mydb.cursor()
    cursor.execute(sql, data)
    mydb.commit()

b2=st.button("View")

if b2:
    show(user_id,complaint,complaint_des,priority,department_id,status)

b1=st.button("Submit")


if b1:
    dump(user_id,complaint,complaint_des,priority,department_id,status)

    st.success("Complaint successfully registered")


