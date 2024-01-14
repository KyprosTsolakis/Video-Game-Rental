#!/usr/bin/env python
# coding: utf-8
# Written by:ID:328778
# Search Game

# In[1]:


import sqlite3

def gameSearch(search_term, conn):
    """
    Search for games in the database based on a search term.

    Args:
        search_term (str): The search term to look for in game titles.
        conn (sqlite3.Connection): The SQLite database connection.

    Returns:
        list: A list of dictionaries representing game information (title, platform, genre).
    """
    search_results = []

    cursor = conn.cursor()

    # Define the SQL query using the LIKE keyword to search for games by title
    query = """
    SELECT title, platform, genre
    FROM Game_Info
    WHERE title LIKE ?
    """

    # Use the '%' wildcard to match any characters before and after the search term
    cursor.execute(query, ('%' + search_term + '%',))

    rows = cursor.fetchall()

    for row in rows:
        title, platform, genre = row
        search_results.append({
            "title": title,
            "platform": platform,
            "genre": genre
        })

    return search_results


# In[ ]:
