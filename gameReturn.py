#!/usr/bin/env python
# coding: utf-8
# Written by:ID:328778
# Returning Games

# In[1]:


import sqlite3

def gameReturn(game_id, conn):
    """
    Return a rented game.

    Args:
        game_id (int): The ID of the game to be returned.
        conn (sqlite3.Connection): The SQLite database connection.

    Returns:
        str: A message indicating the result of the return operation.
    """
    cursor = conn.cursor()

    # Check if the game ID is valid and the game is currently rented
    game_valid, game_rented = is_game_valid_and_rented(game_id, conn)

    if not game_valid:
        return "Invalid game ID. Please provide a valid ID."

    if not game_rented:
        return "The selected game is not currently rented."

    # Perform the return by updating the database records
    update_return_records(game_id, conn)

    return "Game returned successfully."

def is_game_valid_and_rented(game_id, conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM Game_Info WHERE ID = ? AND ID IN (SELECT Game_Id 
                   FROM Rental_History WHERE return_date IS NULL)''', (game_id,))
    game_valid = cursor.fetchone() is not None

    cursor.execute("SELECT 1 FROM Rental_History WHERE game_id = ? AND return_date IS NULL", (game_id,))
    game_rented = cursor.fetchone() is not None

    return game_valid, game_rented

def update_return_records(game_id, conn):
    cursor = conn.cursor()

    # Update the rental record to mark the game as returned
    cursor.execute("UPDATE Rental_History SET return_date = date('now') WHERE game_id = ? AND return_date IS NULL", (game_id,))

    conn.commit()


# In[ ]:




