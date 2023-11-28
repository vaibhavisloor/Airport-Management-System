import streamlit as st
import pandas as pd
import sqlite3


conn = sqlite3.connect('Aerohub.db') 
cursor = conn.cursor() 

# ---------------------------------------------------------------------------------------------

def home_page():
    col1, col2 = st.columns([2, 1]) 

    with col1:
        st.title('Welcome to AeroHub')
        
    with col2:
        st.image('plane.png',width=200)

    st.subheader("Your gateway to the skies ")
    st.title("Today's Outgoing Flight Timings")
    cursor.execute("SELECT * FROM flight_timings")
    flight_records = cursor.fetchall()

    if flight_records:
        df = pd.DataFrame(flight_records, columns=['Flight Number', 'From', 'To', 'Departure Time', 'Arrival Time'])
        new_df = df.sort_values(by="Departure Time", ascending=True)
        st.write(new_df)
    else:
        st.write("No flight timings found.")
    
    st.header("Today's Incoming Flight Timings") 
    cursor.execute("SELECT * FROM flight_timings_incoming")
    flight_records = cursor.fetchall()


    if flight_records:
        df = pd.DataFrame(flight_records, columns=['Flight Number', 'From', 'To', 'Departure Time', 'Arrival Time'])
        new_df = df.sort_values(by="Arrival Time", ascending=True)
        st.write(new_df)
    else:
        st.write("No flight timings found.") 

    st.subheader("Bangalore Aiport Map")     

    st.image("image.png")
    
# -----------------------------------------------------------------------------------
    
def login_page():
    st.title('Login to AeroHub')
    st.write("Please enter your credentials to log in.")

    # Input fields for username and password
    global username,password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2,col3 = st.columns([2, 2,2]) 

    with col1:
        if "user_login_state" not in st.session_state:
            st.session_state.user_login_state = False

        user_login=st.button("User Login")
        
    with col2:
        employee_login=st.button("Employee Login")

    with col3:
        if "admin_login_state" not in st.session_state:
            st.session_state.admin_login_state = False

        admin_login=st.button("Admin Login",key='admin_login_button')

    if user_login or st.session_state.user_login_state:
        st.session_state.user_login_state = True

        query = (f"""SELECT username, password
                    FROM users WHERE (username, password) 
                 = (SELECT ? AS input_username, ? AS input_password);
                """)
        cursor.execute(query,(username,password))
        user = cursor.fetchone()

        if user:
            st.success("Logged in as User")
            user_page()
        else:
            st.error("Invalid username or password")

    if employee_login:
        query = (f"""SELECT username, password
                    FROM employee WHERE (username, password) 
                 = (SELECT ? AS input_username, ? AS input_password);
                """)
        cursor.execute(query,(username,password))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE employee SET attendance=1 WHERE username=? and password=?",(username,password))
            conn.commit()
            st.success(f"Your Attendance has been marked")
        else:
            st.error("Invalid username or password")

    if admin_login or st.session_state.admin_login_state:
        st.session_state.admin_login_state = True
        st.success("Succesfully Logged In")
        query = (f"""SELECT username, password
                    FROM admin WHERE (username, password) 
                 = (SELECT ? AS input_username, ? AS input_password);
                """)
        cursor.execute(query,(username,password))
        user = cursor.fetchone()

        if (user is not None):
            admin_page()
        else:
            st.error("Invalid username or password")

# --------------------------------------------------------------------------------------------------

def user_page():
    st.title('User Dashboard')
    st.write("Welcome to the User Dashboard. You have limited access.")
        
    if "book_flight" not in st.session_state:
        st.session_state.book_flight = False

    
    if st.checkbox("View My Booking"):
            cursor.execute("SELECT * FROM FlightBooking WHERE username=? and password=?",(username,password))
            booking = cursor.fetchone()
            st.write(booking)    
            if st.button("Cancel my reservation"):
                cursor.execute("""DELETE FROM FlightBooking WHERE username = ?""", (username,))
                conn.commit()
                st.success("Booking was successfully cancelled")

    if st.button('Book a Flight') or st.session_state.book_flight:
        st.session_state.book_flight = True
        
        st.header('Flight Booking Form') 
        with st.form(key='flight_booking_form'):
            destination = st.selectbox('Select Destination', ['Delhi','Mumbai', 'Chennai', 'Kolkata', 'Ahmedabad'])
            date = st.selectbox('Select Date', ['2023-11-22','2023-11-23','2023-11-24', '2023-11-25', '2023-11-26'])
            passengers = st.number_input('Number of Passengers', min_value=1, max_value=10, value=1)
            submit_button = st.form_submit_button(label='Book a Flight')

        if submit_button:
            # Fetching user's name
            cursor.execute("SELECT name FROM users WHERE username=? and password=?", (username, password))
            name = str(cursor.fetchone())[2:14]
            # print(name)

            cursor.execute("SELECT departure_time from flights_booking WHERE to_destination=? and departure_date=?",(destination,date))
            dep_time = cursor.fetchone()
            time=dep_time[0]
            query="INSERT INTO FlightBooking (username, password, name, passengers, from_destination, to_destination, flight_date,flight_time) VALUES (?, ?, ?, ?, ?, ?, ?,?)"
            cursor.execute(query,(username, password, name, passengers, "Bangalore", destination, date,time))
            conn.commit()  # Committing the transaction
            st.success("Booking Confirmed")

   
#--------------------------------------------------------------------------------------------------------------------------------------------

def admin_page():
    st.title('Admin Dashboard')
    st.write("Welcome to the Admin Dashboard. You have full access.")

    if st.checkbox("Delete Flight bookings"):
                st.subheader("Delete Flight bookings")
                usn = st.text_input("Username of the Passenger")
                if st.button("Delete Reservation"):
                    if usn:
                        cursor.execute("SELECT username FROM Flightbooking")
                        bookings = cursor.fetchall()
                        names = [result[0] for result in bookings]
                        if usn in names:
                            cursor.execute("DELETE FROM FlightBooking WHERE username=?",(usn,))
                            conn.commit()
                            st.success("Flight Booking has been cancelled")
                        else:
                            st.error("User doesn't have a booking")    
                    else:
                        st.error("Username is empty")        

    if st.checkbox("Modify Flight Timings"):
                destination = st.selectbox('Select Destination', ['Delhi','Mumbai', 'Chennai', 'Kolkata', 'Ahmedabad'])
                date = st.selectbox('Select Date', ['2023-11-22','2023-11-23','2023-11-24', '2023-11-25', '2023-11-26'])
                new_time = st.text_input("Enter Departure Time")
                if st.button("Change Timings"):
                    cursor.execute("UPDATE flights_booking SET departure_time = ? WHERE to_destination = ? and departure_date= ?",(new_time,destination,date))
                    cursor.execute("UPDATE FlightBooking SET flight_time = ? WHERE to_destination = ? and flight_date= ?",(new_time,destination,date))
                    conn.commit()
                    st.success("Flight Timings Successfully changed")

    # with col3:        
    if st.checkbox("Add Employee"):
                st.write("Enter employee credentials")
                name=st.text_input("Employee Name")
                username=st.text_input("Employee Username")
                password=st.text_input("Employee Password")
                if st.button("Add Employee"):
                    cursor.execute("INSERT INTO employee(name,username,password) VALUES (?,?,?)",(name,username,password,))
                    conn.commit()
                    st.success("Employee Added")


    if st.checkbox("Delete Employee"):
                st.write("Enter Employee username") 
                emp_username=st.text_input("Employee Username")
                if st.button("Delete Employee"):
                    cursor.execute("DELETE FROM employee WHERE username=?",(emp_username,))
                    conn.commit()
                    st.success("Employee deleted")

    if st.checkbox("Delete User"):
            st.write("Enter User username") 
            user_username=st.text_input("User Username")
            if st.button("Delete User"):
                cursor.execute("DELETE FROM users WHERE username=?",(user_username,))
                conn.commit()
                st.success("User deleted")

    if st.checkbox("View Attendance") :
            cursor.execute("SELECT name,attendance FROM employee")
            employees = cursor.fetchall()
            st.subheader("Today's Employee Attendance")
            df=pd.DataFrame(employees,columns=['Name','Attendance'])
            st.write(df)
            
    if st.checkbox("View Summary Counts"):
                cursor.execute("SELECT COUNT(name) FROM users")
                users = cursor.fetchone()            
                cursor.execute("SELECT COUNT(name) FROM employee")
                employees = cursor.fetchone()
                cursor.execute("SELECT COUNT(name) FROM admin")
                admin=cursor.fetchone()
                cursor.execute("""SELECT AVG(passengers) FROM FlightBooking""")
                avg_p=cursor.fetchone()
                st.write(f"Total Users: {users[0]}")
                st.write(f"Total Employees: {employees[0]}")
                st.write(f"Total Admins: {admin[0]}")
                st.write(f" Average Number of passengers / Booking :{avg_p[0]}")
        
    if st.checkbox("View Bookings"):
            cursor.execute("SELECT * FROM FlightBooking")
            bookings = cursor.fetchall()
            for booking in bookings:
                st.write(booking)        
    if st.checkbox("View Tables"):
            if st.checkbox("View Users Table"):
                cursor.execute("SELECT name,username,password FROM users")
                users = pd.DataFrame(cursor.fetchall(),columns=["Name","Username","Password"])
                st.write(users)
            if st.checkbox("View Employee Table"):
                cursor.execute("SELECT name,username,password FROM employee")
                employees_data = pd.DataFrame(cursor.fetchall(),columns=["Name","Username","Password"])
                st.write(employees_data)



                
#------------------------------------------------------------------------------------------

def signup_page():
    st.title('SignUp to AeroHub')
    st.write("Please enter your credentials to log in.")

    name_s=st.text_input("Name")
    username_s = st.text_input("Username")
    password_s = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        cursor.execute("""INSERT INTO users(name,username,password) VALUES(?,?,?)""",(name_s,username_s,password_s))
        conn.commit()
        st.success("Successfully Signed Up. Please go to Login page to continue.")

# ------------------------------------------------------------------------------------------

def main():
    nav_option = st.sidebar.radio('Navigation', ('Home', 'Login','SignUp'))

    if nav_option == 'Home':
        home_page()
    elif nav_option == 'Login':
        login_page()
    elif nav_option == 'SignUp':
        signup_page()
        
if __name__ == "__main__":
    main()        

#--------------------------------------------------------------------------------------------


