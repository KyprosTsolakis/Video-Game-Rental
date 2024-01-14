import random
from datetime import datetime, timedelta

# Function to generate a random date within a given range
def random_date(start_date, end_date):
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Define the date range for rental history (adjust as needed)
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 10, 27)

# Number of records to generate
num_records = 200

# Open the file for writing
with open('Rental_History.txt', 'w') as file:
    # Write the header
    file.write("Game ID\tRental Date\tReturn Date\tCustomer ID\n")

    # Generate and write the rental history records
    for game_id in range(1, num_records + 1):
        rental_date = random_date(start_date, end_date).strftime("%d/%m/%Y")
        return_date = random_date(start_date, end_date).strftime("%d/%m/%Y") if random.random() < 0.7 else ""
        customer_id = random.randint(1000, 9999)
        
        record = f"{game_id}\t{rental_date}\t{return_date}\t{customer_id}\n"
        file.write(record)
