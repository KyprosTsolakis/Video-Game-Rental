#!/usr/bin/env python
# coding: utf-8
# Written by:ID:328778
# Database Requirements

# In[1]:


import sqlite3
import pandas as pd
from datetime import datetime


def init_db():
    """
    Initialize the database for the video game rental management system.
    Creates the necessary tables if they don't exist.
    """
    try:
        conn = sqlite3.connect('GameRental.db')
        cursor = conn.cursor()

        # Create the Game_Info table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Game_Info (
                ID INTEGER PRIMARY KEY,
                Platform TEXT,
                Genre TEXT,
                Title TEXT,
                Purchase_Price REAL,
                Purchase_Date DATE
            )
        ''')
        
        
        # Create the Rental_History table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Rental_History (
                Game_ID INTEGER,
                Rental_Date DATE,
                Return_Date DATE,
                Customer_ID INTEGER
            )
        ''')
       
        # Create the Subscription_Info table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Subscription_Info (
                Customer_ID INTEGER,
                Subscription_Type VARCHAR(8),
                Start_Date DATE,
                End_Date DATE
            )
        ''')

      

        # Clean up tables
        cursor.execute("DELETE from Game_Info;")
        cursor.execute("DELETE from Rental_History;")
        cursor.execute("DELETE from Subscription_Info;")
        # Populate tables from text files

        

        conn.commit()
        

        populate_subscription_info_from_text_file(conn)
        populate_game_info_from_text_file(conn)
        populate_rental_history_from_text_file(conn)
        

        
        conn.close()
       
        
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

def write_to_db(df_data, table_name):
    """
    Write a DataFrame to a specific table in the database.
    
    Args:
        df_data (pd.DataFrame): Data to write into the database.
        table_name (str): The name of the database table.
    """
    try:
        conn = sqlite3.connect('GameRental.db')
        df_data.to_sql(table_name, if_exists='replace', index=False, con=conn)
        conn.close()
    except sqlite3.Error as e:
        print(f"Database write error: {e}")

def read_from_db(table_name):
    """
    Read data from a specific table in the database.
    
    Args:
        table_name (str): The name of the database table.
    
    Returns:
        pd.DataFrame: A DataFrame containing the data from the specified table.
    """
    try:
        conn = sqlite3.connect('GameRental.db')
        query = f"SELECT * FROM {table_name}"
        df_data = pd.read_sql(query, con=conn)
        conn.close()
        return df_data
    except sqlite3.Error as e:
        print(f"Database read error: {e}")

def fix_date(datestring):
   
    try:
        date = datetime.strptime(datestring, '%d/%m/%Y')
        return datetime.strftime(date, '%Y-%m-%d')
    except ValueError:
        return None
def data_cleanup(conn):
    """
    Clean up data in the Rental_History table (e.g., handle missing return dates, incorrect data, etc.).
    """
    try:
        #conn = sqlite3.connect('GameRental.db')
        cursor = conn.cursor()
        
        # Example data cleaning: Set missing return dates to NULL
        cursor.execute("UPDATE Rental_History SET Return_Date=NULL WHERE Return_Date='';")
        cursor.execute("UPDATE Rental_History SET Return_Date=Rental_Date, Rental_Date=Return_Date WHERE (Return_Date < Rental_Date);")
        
        conn.commit()
        #conn.close()
    except sqlite3.Error as e:
        print(f"Data cleanup error: {e}")

def populate_game_info_from_text_file(conn):
    cursor = conn.cursor()
    f = 0
    with open('Game_Info.txt', 'r') as file:
        for line in file:
            game_data = line.strip().split(',')
            if len(game_data) == 6  :
                if f==0 :
                    f=1
                else : 
                    id, platform, genre, title, purchase_price, purchase_date = game_data
                    cursor.execute(
                        "INSERT INTO Game_Info (id, Platform, Genre, Title, Purchase_Price, Purchase_Date) VALUES (?, ?, ?, ?, ?, ?)",
                        (id, platform, genre, title, purchase_price, purchase_date)
                    )

    conn.commit()

def populate_rental_history_from_text_file(conn):
    cursor = conn.cursor()
    f = 0
    with open('Rental_History.txt', 'r') as file:
        for line in file:
            rental_data = line.strip().split(',')
            if len(rental_data) == 4:
                if f==0 :
                    f=1
                else :
                    game_id, rental_date, return_date, customer_id = rental_data
                    
                     
                    rental_date = fix_date(rental_date)
                    return_date = fix_date(return_date)

                    cursor.execute(
                        "INSERT INTO Rental_History (game_id, rental_date, return_date, customer_id) VALUES (?, ?, ?, ?)",
                        (game_id, rental_date, return_date, customer_id)
                    )

    conn.commit()
    # Fix Dates
    data_cleanup(conn)


def populate_subscription_info_from_text_file(conn):
    cursor = conn.cursor()
    f = 0
    with open('Subscription_Info.txt', 'r') as file:
        for line in file:
            subscription_data = line.strip().split(',')
            if len(subscription_data) == 4:
                if f==0 :
                    f=1
                else :
                    Customer_ID,Subscription_Type,Start_Date,End_Date = subscription_data
                 

                    cursor.execute(
                        "INSERT INTO Subscription_Info (Customer_ID,Subscription_Type,Start_Date,End_Date) VALUES (?, ?, ?, ?)",
                        (Customer_ID,Subscription_Type,Start_Date,End_Date)
                    )

    conn.commit()

# In[ ]:




