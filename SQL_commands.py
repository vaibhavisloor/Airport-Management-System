import sqlite3

conn = sqlite3.connect('Aerohub.db')
cursor = conn.cursor()


# USERS TABLE

cursor.execute("""
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
""")

conn.commit()



# EMPLOYEE TABLE

cursor.execute("""CREATE TABLE employee (
    empid INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    attendance INT DEFAULT NULL
 );
 """)
conn.commit()



# ADMIN TABLE

cursor.execute("""
CREATE TABLE admin (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
""")
conn.commit()



# INCOMING FLIGHTS TABLE

cursor.execute("""
CREATE TABLE flight_timings_incoming (
    flight_number VARCHAR(10),
    from_destination VARCHAR(50),
    to_destination VARCHAR(50),
    departure_time TIME,
    arrival_time TIME
);
""")
conn.commit()



# OUTGOING FLIGHTS TABLE

cursor.execute("""
CREATE TABLE flight_timings (
    flight_number VARCHAR(10),
    from_destination VARCHAR(50),
    to_destination VARCHAR(50),
    departure_time TIME,
    arrival_time TIME
);
""")
conn.commit()



# TABLE FLIGHTS AVAILABLE FOR BOOKING

cursor.execute("""
CREATE TABLE flights_booking (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    from_destination VARCHAR(50),
    to_destination VARCHAR(50),
    departure_date DATE,
    departure_time TIME
);
""")
conn.commit()



# BOOKING DETAILS  TABLE

cursor.execute("""CREATE TABLE FlightBooking (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    passengers INT NOT NULL,
    from_destination VARCHAR(50) NOT NULL,
    to_destination VARCHAR(50) NOT NULL,
    flight_date DATE NOT NULL,
    flight_time TIME NOT NULL
);
""")
conn.commit()



# DML STATEMENTS


# ADDING USERS TO TABLE

cursor.execute("""INSERT INTO users (name, username, password)
VALUES
    ('Rajesh Kumar', 'rajeshkumar123', 'password123'),
    ('Priya Patel', 'priyapatel456', 'securepass'),
    ('Amit Singh', 'amitsingh789', 'safepassword'),
    ('Deepika Mishra', 'deepikamishra01', 'strongpass123'),
    ('Rahul Sharma', 'rahul_sharma', 'mysecurepw'),
    ('Ananya Verma', 'ananyav_22', 'p@ssw0rd!'),
    ('Sandeep Gupta', 'sandeepg99', 'guptaPass'),
    ('Neha Joshi', 'neha.joshi', 'joshiPass'),
    ('Karthik Reddy', 'karthikr', 'reddy123'),
    ('Pooja Khanna', 'pooja_kh', 'khanna567');
""")
conn.commit()


# ADDING EMPLOYEES TO TABLE

cursor.execute(""" INSERT INTO employee (username, name, password)
VALUES
    ('john123', 'John Doe', 'pass123'),
    ('alice456', 'Alice Smith', 'secure456'),
    ('bob789', 'Bob Johnson', 'safe789'),
    ('emily01', 'Emily Davis', 'strong01'),
    ('michael22', 'Michael Wilson', 'my123'),
    ('sophia333', 'Sophia Brown', 'passw0rd!'),
    ('david444', 'David Lee', 'davidpass'),
    ('olivia567', 'Olivia Garcia', 'garcia567'),
    ('ethan88', 'Ethan Martinez', 'ethanpass'),
    ('ava99', 'Ava Anderson', 'anderson99');
""")
conn.commit()


# ADDING ADMINS TO TABLE

cursor.execute("""INSERT INTO admin (name, username, password)
VALUES
    ('Aditi Sharma', 'aditi_admin', 'adminpass1'),
    ('Vikram Singh', 'vikram_admin', 'adminpass2'),
    ('Neha Patel', 'neha_admin', 'adminpass3'),
    ('Rajesh Khanna', 'rajesh_admin', 'adminpass4'),
    ('Ananya Gupta', 'ananya_admin', 'adminpass5');
""")
conn.commit()


# ADDING FLIGHTS WHICH CAN BE BOOKED BY USERS

cursor.execute("""INSERT INTO flights_booking (from_destination, to_destination, departure_date, departure_time) VALUES
    -- Bangalore to Delhi 
    ( 'Bangalore', 'Delhi', '2023-11-22', '08:00:00'),
    ( 'Bangalore', 'Delhi', '2023-11-23', '10:30:00'),
    ( 'Bangalore', 'Delhi', '2023-11-24', '12:45:00'),
    ( 'Bangalore', 'Delhi', '2023-11-25', '15:20:00'),
    ( 'Bangalore', 'Delhi', '2023-11-26', '18:00:00'),
    
    -- Bangalore to Mumbai 
    ( 'Bangalore', 'Mumbai', '2023-11-22', '09:15:00'),
    ( 'Bangalore', 'Mumbai', '2023-11-23', '11:45:00'),
    ( 'Bangalore', 'Mumbai', '2023-11-24', '14:00:00'),
    ( 'Bangalore', 'Mumbai', '2023-11-25', '16:30:00'),
    ( 'Bangalore', 'Mumbai', '2023-11-26', '19:15:00'),
    
    -- Bangalore to Chennai 
    ( 'Bangalore', 'Chennai', '2023-11-22', '10:00:00'),
    ( 'Bangalore', 'Chennai', '2023-11-23', '12:30:00'),
    ( 'Bangalore', 'Chennai', '2023-11-24', '14:45:00'),
    ( 'Bangalore', 'Chennai', '2023-11-25', '17:10:00'),
    ( 'Bangalore', 'Chennai', '2023-11-26', '20:00:00'),
    
    -- Bangalore to Kolkata 
    ( 'Bangalore', 'Kolkata', '2023-11-22', '11:30:00'),
    ( 'Bangalore', 'Kolkata', '2023-11-23', '13:45:00'),
    ( 'Bangalore', 'Kolkata', '2023-11-24', '16:00:00'),
    ( 'Bangalore', 'Kolkata', '2023-11-25', '18:30:00'),
    ( 'Bangalore', 'Kolkata', '2023-11-26', '21:15:00'),
    
    -- Bangalore to Ahmedabad 
    ( 'Bangalore', 'Ahmedabad', '2023-11-22', '12:45:00'),
    ( 'Bangalore', 'Ahmedabad', '2023-11-23', '15:00:00'),
    ( 'Bangalore', 'Ahmedabad', '2023-11-24', '17:30:00'),
    ( 'Bangalore', 'Ahmedabad', '2023-11-25', '19:45:00'),
    ( 'Bangalore', 'Ahmedabad', '2023-11-26', '22:00:00');
""")
conn.commit()

# ADDING INCOMING AND OUTGOING FLIGHT DETAILS


cursor.execute("""INSERT INTO flight_timings (flight_number, from_destination, to_destination, departure_time, arrival_time)
VALUES
    ('FL001', 'Bangalore', 'Delhi', '08:00:00', '11:00:00'),
    ('FL002', 'Bangalore', 'Mumbai', '14:30:00', '16:00:00'),
    ('FL003', 'Bangalore', 'Chennai', '17:45:00', '23:30:00'),
    ('FL004', 'Bangalore', 'Kolkata', '09:15:00', '16:45:00'),
    ('FL005', 'Bangalore', 'Hyderabad', '12:00:00', '13:30:00'),
    ('FL006', 'Bangalore', 'Jaipur', '10:20:00', '12:00:00'),
    ('FL007', 'Bangalore', 'Ahmedabad', '08:45:00', '10:30:00'),
    ('FL008', 'Bangalore', 'Pune', '15:00:00', '18:30:00'),
    ('FL009', 'Bangalore', 'Lucknow', '13:20:00', '14:45:00'),
    ('FL010', 'Bangalore', 'Patna', '19:30:00', '22:15:00');
""")
conn.commit()

cursor.execute("""INSERT INTO flight_timings_incoming (flight_number, from_destination, to_destination, departure_time, arrival_time)
VALUES
    ('FL001', 'Delhi', 'Bangalore', '08:30:00', '11:30:00'),
    ('FL002', 'Mumbai', 'Bangalore', '15:00:00', '16:30:00'),
    ('FL003', 'Chennai', 'Bangalore', '18:15:00', '00:00:00'),
    ('FL004', 'Kolkata', 'Bangalore', '09:45:00', '17:15:00'),
    ('FL005', 'Hyderabad', 'Bangalore', '12:30:00', '14:00:00'),
    ('FL006', 'Jaipur', 'Bangalore', '10:50:00', '12:30:00'),
    ('FL007', 'Ahmedabad', 'Bangalore', '09:15:00', '11:00:00'),
    ('FL008', 'Pune', 'Bangalore', '15:45:00', '19:15:00'),
    ('FL009', 'Lucknow', 'Bangalore', '13:40:00', '15:05:00'),
    ('FL010', 'Patna', 'Bangalore', '20:00:00', '22:45:00');

""")
conn.commit()
