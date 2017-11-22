
import csv
import sqlite3


def get_tickers():
    # Variables
    tickers = []
    filename = 'data/etf-list/active_etfs.json'

    # Open file and extract tickers
    with open(filename, "r") as f:
        for line in f:
            split_line = line.split(',')
            ticker = split_line[0].replace('-', '_')    # Replace - with _ because of db table name
            tickers.append(ticker)

    return tickers


def store_etfs():
    # Get ticker
    tickers = get_tickers()
    print(tickers)

    # Create db tables
    for i in range(len(tickers)):
        create_table(tickers[i])
        print("Table for ticker " + tickers[i] + " has been created.")

    # Insert historical value entries into database
    for i in range(len(tickers)):
        insert_db(tickers[i])
        print("Entries for ticker " + tickers[i] + " has been inserted into db.")


def create_table(ticker):
    # Start connection
    connection = sqlite3.connect('data/db/database.db')

    # Drop table
    sql_cmd_dt = '''DROP TABLE IF EXISTS {}'''.format(ticker)
    connection.execute(sql_cmd_dt)

    # Create table
    sql_cmd_ct = '''CREATE TABLE {}(date int primary key not null, open, high, low, close, volume, value)'''.format(ticker)
    connection.execute(sql_cmd_ct)

    # Close connection
    connection.close()


def insert_db(ticker):
    # Filename for historical values
    filename = 'data/historical-values/' + ticker.replace('_', '-') + '.csv'

    # Start connection
    connection = sqlite3.connect('data/db/database.db')

    # Read and execute insertion
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)        # Skip the first line
        for i, line in enumerate(reader):
            try:
                connection.execute("INSERT INTO {} (date,open,high,low,close,volume,value) VALUES ({},{},{},{},{},{},{})".format(ticker, line[0], line[3], line[4], line[5], line[6], line[7], line[8]))
            except:
                print("Entries for ticker " + ticker + ", date: " + line[0] + " already exist.")

    # Commit inserts
    connection.commit()

    # Close connection
    connection.close()


def select_db(ticker):
    # Variable for content
    db_content = []

    # Start connection
    connection = sqlite3.connect('data/db/database.db')

    # Selection command
    sql_cmd_s = connection.execute("SELECT date, open, high, low, close, volume, value from {}".format(ticker))

    # Append data to list
    for row in sql_cmd_s:
        db_content.append(row)

    # Close connection
    connection.close()

    # Return historical values
    return db_content
