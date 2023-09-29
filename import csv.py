import csv
import sqlite3

# Create a connection to the sqlite database.
conn = sqlite3.connect('mydb.sqlite')

# Open the csv file.
with open('C:\\Users\\kingl\\Downloads\\ipc-county\\data\\Project_Data.csv', 'r') as csvfile:

    # Read the csv file into a list of tuples.
    reader = csv.reader(csvfile)
    data = list(reader)

    # Insert the tuples into the sqlite database.
    conn.execute('CREATE TABLE mytable')
    for row in data:
        
        conn.execute('INSERT INTO mytable (FIPS_Code, States, Area_Name, Civilian_labor_force_2020, Employed_2020, Unemployed_2020, Unemployment_rate_2020, Civilian_labor_force_2021, Employed_2021, Unemployed_2021, Unemployment_rate_2021, Civilian_labor_force_2022, Employed_2022, Unemployed_2022, Unemployment_rate_2022, POP_ESTIMATE_2020, POP_ESTIMATE_2021, POP_ESTIMATE_2022, BIRTHS_2020, BIRTHS_2021, BIRTHS_2022, DEATHS_2020, DEATHS_2021, DEATHS_2022, NoHSD, HSD, CAD, BD) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)

# Close the csv file.
csvfile.close()

# Close the connection to the sqlite database.
conn.close()