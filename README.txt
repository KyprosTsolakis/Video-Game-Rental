Video Game Rental Management System
Program Description:
The Video Game Rental Management System is a Python-based application implemented within Jupyter notebooks. Developed by Kypros (ID:328778) in November 2023, 
the system utilizes an SQLite database to manage information related to video game rentals, customer subscriptions, and game inventory. 
The program offers functionalities such as game search, rental, return, purchase recommendations, and database initialization.
How to Use:

Initialize Database:
Click the "Initialize Database" button to set up the SQLite database.
This operation clears existing data in tables (Game_Info, Rental_History, Subscription_Info) 
and populates them with sample data from text files (Game_Info.txt, Rental_History.txt, Subscription_Info.txt).

Search Games:
Enter a search term in the "Search Term" input box.
Click the "Search Games" button to find games containing the search term in their titles.
The search results will be displayed in the output area.
Rental_History.py is how I created the Rental_History.txt with Python.

Rent Game:
Enter the customer ID and game ID in the respective input boxes.
Click the "Rent Game" button to rent a game to the customer.
The program performs checks such as valid customer ID, valid game ID, and subscription compatibility before processing the rental.

Return Game:
Enter the game ID in the "Return Game ID" input box.
Click the "Return Game" button to mark a rented game as returned.
The program checks if the game is valid and currently rented before processing the return.

Create Purchase Order:
Enter the budget in the "Budget (£)" input box.
Click the "Create Purchase Order" button to generate game purchase recommendations based on popularity and budget constraints.
The recommendations include game titles and genres that can be purchased within the specified budget.

Clear Output:
Click the "Clear" button to clear the output area.

Sumbitted the subscriptionManager.pyc and the Subscription_Info.txt because I used to for my code.
Submitted the __pycache__ folder and .ipynb_checkpoints folder becuase I tested if it works. 
You can delete them and re-created after you run the code for menu.ipynb
intialized the db and try out the GUI.For my code is better to return the game First example ID of the game=3 and the Rent it.
Added also the Rental_History.py to show how I created my Rental_History.txt file
