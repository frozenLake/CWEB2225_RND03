from datetime import datetime

import mysql.connector
from mysql.connector import Error
from select import select
import re
import pandas as pd

#MySQL connection
connection_params = {

    'host': 'localhost',
    'database': 'hw04database',
    'user': 'new_username1',
    'password': 'new_password1'
}

def main():
    ensure_table_exists()

    while True:
        print("Choose an operation:")
        print("1. Create a record")
        print("2. Read records")
        print("3. Update a record")
        print("4. Delete a record")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            create_record()
        elif choice == "2":
            read_records()
        elif choice == "3":
            update_record()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

def ensure_table_exists():
    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS user(
			id INT AUTO_INCREMENT PRIMARY KEY,
			name VARCHAR(100) NOT NULL,
			email VARCHAR(255) NOT NULL,
			phone VARCHAR(100) NOT NULL,
			address VARCHAR(255) NOT NULL,
			created_at DATETIME
			); """
            cursor.execute(create_table_query)
            conn.commit()
            print("Table 'user' is ensured to exist")
    except Error as e:
        print("Error: ",e)

#done
def create_record():
    name = input("Enter name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter name: ").strip()

    email = input("Enter email: ").strip()
    while not email or not bool(re.search("^(.+)@(\\S+)$",email)):
        print("Please enter a valid email.")
        email = input("Enter email: ").strip()

    phone = input("Enter phone: ").strip()
    while not phone or not re.search(r'^\d{10,}$',phone):
        print("Please enter a valid phone number.")
        phone = input("Enter phone: ").strip()

    address = input("Enter address: ").strip()
    while not address:
        print("Address cannot be empty.")
        address = input("Enter address: ").strip()

    created_at = datetime.now()

    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            query = "INSERT INTO USER (name, email, phone, address, created_at) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, email, phone, address, created_at))
            conn.commit()
            print("Record inserted successfully. ")

    except Error as e:
        print("Error: ",e)

#go back to
def read_records():
    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM USER"
            cursor.execute(query)
            rows = cursor.fetchall()
            print(f"{'ID':<5} {'Name':<20} {'Email':<20} {'Phone':<15} {'Address':<20} {'Created At':<30}")
            print("-"*115)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20} {row[3]:<15} {row[4]:<20} {row[5]}")
    except Error as e:
        print("Error: ",e)

#to do
def update_record():
    record_id = input("Enter the ID of the person to update: ").strip()
    while not record_id.isdigit():
        print("Please enter a valid ID.")
        record_id = input("Enter the ID of the person to update: ").strip()
    record_id = int(record_id)

    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            select_query = "SELECT * FROM user WHERE ID = %s"
            cursor.execute(select_query, (record_id,))
            rows = cursor.fetchone()
            if not rows:
                print("No record found with ID: ", record_id)
                return

            new_name = input("Enter new name: ").strip()
            while not new_name:
                print("Name cannot be empty.")
                new_name = input("Enter new name: ").strip()

            new_email = input("Enter new email: ").strip()
            while not new_email or not bool(re.search("^(.+)@(\\S+)$", new_email)):
                print("Please enter a valid email.")
                new_email = input("Enter email: ").strip()

            new_phone = input("Enter new phone number: ").strip()
            while not new_phone or not re.search(r'^\d{10,}$', new_phone):
                print("Please enter a valid phone number.")
                new_phone = input("Enter phone: ").strip()

            new_address = input("Enter new address: ").strip()
            while not new_address:
                print("Address cannot be empty.")
                new_address = input("Enter address: ").strip()

            update_query = "UPDATE USER SET name=%s, email=%s, phone=%s, address=%s WHERE ID=%s"
            cursor.execute(update_query, (new_name, new_email, new_phone, new_address, record_id))
            conn.commit()
            if cursor.rowcount > 0:
                print("Record updated successfully.")
            else:
                print("No records updated...")
    except Error as e:
        print("Error: ",e)

#done
def delete_record():
    delete_id = input("Enter the ID of the person to delete: ").strip()
    while not delete_id.isdigit():
        print("Please enter a valid ID.")
        delete_id = input("Enter the ID of the person to delete: ").strip()
    delete_id = int(delete_id)

    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            delete_query = "DELETE FROM USER WHERE ID = %s"
            cursor.execute(delete_query, (delete_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print("Record deleted successfully.")
            else:
                print("No records deleted...")

    except Error as e:
        print("Error: ",e)

main()