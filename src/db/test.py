import pandas as pd
import sqlite3

# Read the CSV file into a DataFrame
df = pd.read_csv('C:\\Users\\benny\\Github\\ipc-county\\data\\Project_Data2.csv')

# Create a SQLite database and a connection to it
conn = sqlite3.connect('project3.sqlite')

# Write the DataFrame to a new table in the SQLite database
df.to_sql('counties', conn, index=False)

# Close the database connection
conn.close()