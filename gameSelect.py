#!/usr/bin/env python
# coding: utf-8
# Written by:ID:328778
# Game Select

# In[1]:


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def gameSelect(budget, conn):
    """
    Recommend game titles and genres for purchase based on a given budget.

    Args:
        budget (float): The budget available for new acquisitions.
        conn (sqlite3.Connection): The SQLite database connection.

    Returns:
        dict: A dictionary containing recommended game titles, genres, and the number of copies to purchase.
    """
    cursor = conn.cursor()

    # Calculate the popularity of game titles and genres
    game_popularity = calculate_game_popularity(conn)
    genre_popularity = calculate_genre_popularity(conn)

    # Sort game titles and genres by popularity
    sorted_games = sorted(game_popularity.items(), key=lambda x: x[1], reverse=True)
    sorted_genres = sorted(genre_popularity.items(), key=lambda x: x[1], reverse=True)

    df = pd.DataFrame({'Game Titles': [game[0] for game in sorted_games],
                       #'Genre': [genre[0] for genre in sorted_genres],
                       'Popularity': [game[0] for game in sorted_games]
                       })


    # Plot the popularity of game titles
    plt.figure(figsize=(10, 20))
    plt.bar(df['Game Titles'], df['Popularity'])
    plt.title('Game Titles Popularity')
    plt.xlabel('Game Titles')
    plt.ylabel('Popularity')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Recommend game titles and genres based on budget
    recommended_games = []
    recommended_genres = []
    total_budget = budget

    for game, popularity in sorted_games:
        game_cost = calculate_game_cost(game, conn)
        if game_cost <= total_budget:
            recommended_games.append((game, popularity))
            total_budget -= game_cost

    for genre, popularity in sorted_genres:
        genre_cost = calculate_genre_cost(genre, conn)
        if genre_cost <= total_budget:
            recommended_genres.append((genre, popularity))
            total_budget -= genre_cost

    recommendations = {
        'Game Titles': recommended_games,
        'Genres': recommended_genres
    }

    return recommendations

def calculate_game_popularity(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT title, COUNT(*) as popularity FROM Rental_History 
                   INNER JOIN Game_Info ON Rental_History.game_id = Game_Info.ID GROUP BY title''')
    game_popularity = {title: popularity for title, popularity in cursor.fetchall()}
    return game_popularity

def calculate_genre_popularity(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT genre, COUNT(*) as popularity FROM Game_Info GROUP BY genre")
    genre_popularity = {genre: popularity for genre, popularity in cursor.fetchall()}
    return genre_popularity

def calculate_game_cost(game, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT purchase_price FROM Game_Info WHERE title = ?", (game,))
    purchase_price = cursor.fetchone()[0]
    return purchase_price

def calculate_genre_cost(genre, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(purchase_price) FROM Game_Info WHERE genre = ?", (genre,))
    average_purchase_price = cursor.fetchone()[0]
    return average_purchase_price


# In[ ]:




