
import sys
import os.path

from download import download_etfs
from database import store_etfs
from rating import rate_etfs


def initialize(arg):
    ticker = arg[1].replace('-', '_')
    method = arg[2]

    try:
        update = arg[3]
    except:
        update = ''


    run(ticker, method, update)


def run(ticker, method, update):

    if update == 'upd' or not os.path.exists('data/db/database.db'):
        # Download ETFs and store into databases
        download_etfs()

        # Store historical data into sqlite3 database
        store_etfs()


    # Perform rating
    rate_etfs(ticker, method)

    return True

if __name__ == "__main__":
    initialize(sys.argv)
