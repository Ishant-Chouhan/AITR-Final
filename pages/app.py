import streamlit as st
import mysql.connector as myconn
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import smtplib

server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
def send_mail(sender,sender_pass,reciever,message):
    server.login(sender,sender_pass)
    server.sendmail(sender,reciever,message)
    print("mail sent successfully")

st.set_page_config(layout="wide")
# Function to fetch data from the MySQL database
def fetch_complaint():
    mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM complaints")
    columns = ["User_id", "Complaint_id", "Complaints", "Priority", "Department_id", "Status"]
    data = cursor.fetchall()
    
    # Convert data to DataFrame
    data = pd.DataFrame(data, columns=columns)
    
    cursor.close()
    mydb.close()
    
    return data

def fetch_dep_com():
    mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
    cursor = mydb.cursor()
    cursor.execute("select * from complaints inner join department_info using (Department_id) inner join user_info using (user_id)")
    data=cursor.fetchall()
    columns=["User_id","Department_id","Complaint_id","Complaint","Priority","Status","Department","govEmail","govPassword","Username","Mobile","Address","Email user","password user"]
    data=pd.DataFrame(data,columns=columns)
    cursor.close()
    mydb.close()
    return data
    
def change_status(complaint_id):
    mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
    cursor = mydb.cursor()
    cursor.execute("UPDATE complaints SET Status = 'Completed' WHERE Complaint_id = %s", (complaint_id,))
    mydb.commit()  # Commit the changes to the database
    cursor.close()
    mydb.close()
# Function to create bar chart
def create_bar_chart(data):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.countplot(data=data, x="Status", palette="viridis", hue="Status", legend=False, ax=ax)
    
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')
    
    ax.set_title("Number of Complaints by Status")
    ax.set_xlabel("Complaint Status")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    return fig

# Function to create pie chart
def create_pie_chart(data):
    priority_counts = data["Priority"].value_counts()
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(priority_counts.values, labels=priority_counts.index, 
           autopct='%1.1f%%', startangle=140)
    ax.set_title("Priority Distribution")
    
    return fig

# Streamlit UI
st.title("Government Complaints Dashboard")

data = fetch_complaint()

def plot_priority():
    mydb = myconn.connect(host="localhost", user="root", password="Cybrom#1123", database="GovComplaints")
    cursor = mydb.cursor()
    
    cursor.execute("SELECT DISTINCT RIGHT(Address,6) FROM user_info")
    d = cursor.fetchall()
    d = pd.DataFrame(d, columns=["Pincode"])  # Ensure correct column name
    
    if not d.empty:
        l = d["Pincode"].tolist()
        b = st.selectbox("Select Pincode:", l)
        
        if b:
            sql = f"""WITH cte AS (
                        SELECT * FROM complaints INNER JOIN user_info USING (user_id)
                      )
                      SELECT RIGHT(Address,6) AS Pincode, department_id, COUNT(*) AS Problem_count 
                      FROM cte 
                      WHERE RIGHT(Address,6) = '{b}'
                      GROUP BY department_id, Pincode"""
            
            cursor.execute(sql)
            dtemp = cursor.fetchall()
            dtemp = pd.DataFrame(dtemp, columns=["Pincode", "Department_id", "Problem_count"])
            
            if not dtemp.empty:
                fig, ax = plt.subplots(figsize=(2,1.5))
                sns.barplot(data=dtemp, x="Department_id", y="Problem_count", palette="viridis", ax=ax)
                
                #  # Small vertical labels
                
                ax.set_title("Problem Count by Department",fontsize=6)
                ax.set_xlabel("Department ID",fontsize=5)
                ax.set_ylabel("Problem Count",fontsize=5)
                ax.tick_params(axis='both', labelsize=4)
                ax.grid(axis="y", linestyle="--", alpha=0.5)
                
                cursor.close()
                mydb.close()
                
                return fig  # Return figure for Streamlit
            else:
                st.warning(f"No data found for Pincode {b}.")
    else:
        st.warning("No pincodes found in the database.")
    
    cursor.close()
    mydb.close()
    return None  # Return None if no figure is generated

# Display in Streamlit
st.write("#### Problem Count by Pincode")
fig = plot_priority()
if fig:
    st.pyplot(fig)  # Show the plot if available

st.markdown(
    """
    <div style="text-align: center; font-size: 10px; font-weight: bold; font-family: 'Times New Roman';">
        1 - Police Department, 2 - Cyber Crime Department, 3 - Women Helpline, 4 - Fire Department, 5 - Consumer Protection Department, 
        6 - Child Welfare Department, 7 - Traffic Police Department, 8 - Social Welfare Department, 9 - Disaster Management, 
        10 - Anti-Corruption Bureau, 11 - Human Rights Department, 12 - Municipal Corporation Department
    </div>
    """,
    unsafe_allow_html=True
)


if not data.empty:
    st.write("### Complaints Analysis")

    # Create two columns
    col1, col2 = st.columns(2)

    # Display bar chart in first column
    with col1:
        st.write("#### Complaints Status Distribution")
        st.pyplot(create_bar_chart(data))

    # Display pie chart in second column
    with col2:
        st.write("#### Priority Distribution")
        st.pyplot(create_pie_chart(data))


    

    d1=fetch_dep_com()
    l = list(d1["Department"].unique())
    l.insert(0, "Search for Department")

# Select department
    option1 = st.selectbox("#### Search for Department", l)
    st.markdown(
    """
    <style>
        .dataframe th, .dataframe td {
            font-family: 'Times New Roman', Times, serif !important;
        }
    </style>
    """,
    unsafe_allow_html=True
    )
# Function to apply color based on status
    def highlight_status(val):
        if val == "Completed":
            color = "color: blue; font-weight: bold; font-family: 'Times New Roman';"
        elif val == "In Progress":
            color = "color: orange; font-weight: bold; font-family: 'Times New Roman';"
        else:
            color = "font-family: 'Times New Roman';"  # Default font
        return color

    def highlight_priority(val):
        if val == "Emergency":
            return "color: red; font-weight: bold; font-family: 'Times New Roman';"
        elif val == "Moderate":
            return "color: orange; font-weight: bold; font-family: 'Times New Roman';"
        elif val == "Less Priority":
            return "color: green; font-weight: bold; font-family: 'Times New Roman';"
        return "font-family: 'Times New Roman';"
    
# Display filtered data with color formatting
    if option1 != "Search for Department":
        df_filtered = d1[d1["Department"] == option1][
            ["User_id", "Complaint_id", "Complaint", "Department_id", "Department", "Priority", "Status", "Username", "Mobile", "Address", "Email user"]
        ]
    
    # Apply styling
        styled_df = df_filtered.style.applymap(highlight_status, subset=["Status","Complaint"])\
                                 .applymap(highlight_priority, subset=["Priority"])
    
    # Show in Streamlit
        st.dataframe(styled_df)


    l1=list(d1["User_id"].unique())
    l1.insert(0,"Search for User ID")
    option2=st.selectbox("#### search for User ID",l1)
    if option2 != "search for User":
        st.write(d1[d1["User_id"]==option2][["User_id","Complaint_id","Complaint","Department_id","Department","Priority","Status","Username","Mobile","Address","Email user"]])


    l2=list(d1["Complaint_id"].unique())
    l2.insert(0,"Search for Complaint ID")
    option3=st.selectbox("#### search for Complaint",l2)
    if option3 != "Search for Complaint ID":
        st.write(d1[d1["Complaint_id"]==option3][["User_id","Complaint_id","Complaint","Department_id","Department","Priority","Status","Username","Mobile","Address","Email user"]])
        b=st.button("Change Status")
        if b:
            change_status(int(option3))
            st.write(f"Status of {option3} has been successfully changed to Completed")
            send_mail(
    d1.loc[d1["Complaint_id"] == option3, "govEmail"].iloc[0],  # Extract single value
    d1.loc[d1["Complaint_id"] == option3, "govPassword"].iloc[0],
    d1.loc[d1["Complaint_id"] == option3, "Email user"].iloc[0],
    f"Dear User, your complaint ID {option3} is successfully resolved by {d1.loc[d1['Complaint_id'] == option3, 'Department'].iloc[0]}"
)

        else:
            st.warning("No complaint data found in the database.")

