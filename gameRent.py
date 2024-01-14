#!/usr/bin/env python
# coding: utf-8
# Written by:ID:328778
# Renting Games

# In[1]:


import sqlite3

BASIC_LIMIT = 2
PREMIUM_LIMIT = 5


def gameRent(customer_id, game_id, conn):
    """
    Rent a game to a customer.

    Args:
        customer_id (int): The ID of the customer.
        game_id (int): The ID of the game to be rented.
        conn (sqlite3.Connection): The SQLite database connection.

    Returns:
        str: A message indicating the result of the rental operation.
    """
    cursor = conn.cursor()

    # Check if the customer and game IDs are valid
    customer_valid = is_customer_valid(customer_id, conn)
    game_valid, game_available = is_game_valid_and_available(game_id, conn)

    if not customer_valid:
        return "Invalid customer ID. Please provide a valid ID."

    if not game_valid:
        return "Invalid game ID. Please provide a valid ID."

    if not game_available:
        return "The selected game is not available for rent."

    # Check if the customer's subscription allows for the rental

    if not is_subscription_valid(customer_id, game_id, conn):
        return "The customer's subscription does not allow renting this game."

    # Perform the rental by updating the database records

    update_rental_records(customer_id, game_id, conn)

    return "Game rented successfully."

def is_customer_valid(customer_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Subscription_Info WHERE Customer_id = ?", (customer_id,))
    return cursor.fetchone() is not None

def is_game_valid_and_available(game_id, conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM Game_Info WHERE 
                   ID = ? AND ID NOT IN 
                   (SELECT Game_Id FROM Rental_History WHERE return_date IS NULL)''', (game_id,))
    
    game_valid = cursor.fetchone() is not None

    cursor.execute('''SELECT 1 FROM Game_Info WHERE ID = ? 
                   AND ID NOT IN 
                   (SELECT Game_Id FROM Rental_History WHERE return_date IS NULL)''', (game_id,))
    
    game_available = cursor.fetchone() is not None
    return game_valid, game_available

def is_subscription_valid(customer_id, game_id, conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM Subscription_Info WHERE 
                   customer_id = ? AND Start_Date <= DATE('now') AND End_Date >= DATE('now') ''', (customer_id,))
    valid_subscription = cursor.fetchone() is not None

    if valid_subscription:
        cursor.execute('''SELECT 1 FROM Game_Info WHERE ID = ? AND ID NOT IN 
                       (SELECT game_id FROM Rental_History WHERE return_date IS NULL) 
                       AND purchase_price >= (SELECT IFNULL(SUM(purchase_price),0) FROM 
                       Game_Info,Rental_History WHERE Game_ID=ID and customer_id = ?
                       AND return_date IS NULL);''', (game_id, customer_id))
        return cursor.fetchone() is not None
    else:
        return False

def update_rental_records(customer_id, game_id, conn):
    cursor = conn.cursor()

    # Insert a new rental record
    cursor.execute("INSERT INTO Rental_History (game_id, rental_date, customer_id) VALUES (?, date('now'), ?)", 
                   (game_id, customer_id))
    conn.commit()

def get_subscription_type(customer_id):

    with open('Subscription_Info.txt', 'r') as file:
        for line in file:
            customer_data = line.strip().split(',')
            if customer_data[0] == str(customer_id):
                return customer_data[1]  # SubscriptionType
    return None  # Customer not found in Subscription_Info.txt

def check_rental_limit(customer_id, subscription_type, conn):
    
    # Return the remaining rental limit for the customer
    if subscription_type == 'Basic':
        rental_limit = BASIC_LIMIT
    elif subscription_type == 'Premium':
        rental_limit = PREMIUM_LIMIT
    else:
        return 0  # Unknown subscription type

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Rental_History WHERE Customer_Id = ? AND Return_Date IS NULL", (customer_id,))
    rented_games = cursor.fetchone()[0]

    return rental_limit - rented_games
    conn.commit()


# In[ ]:




