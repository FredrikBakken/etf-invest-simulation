
import sys

from download import download_etfs
from database import get_tickers, store_etfs, select_db
from rating import rate_etfs


def initialize(arg):
    ticker = arg[1].replace('-', '_')
    method = arg[2]

    run(ticker, method)


def run(ticker, method):
    # Download ETFs and store into databases
    # download_etfs()

    # Store historical data into sqlite3 database
    # store_etfs()
    # db_content = select_db('AI_ABNIG')
    # print(db_content)

    # Perform rating
    rate_etfs(ticker, method)

    '''
    tickers = get_tickers()
    print(tickers)

    # Create db tables
    for i in range(len(tickers)):
        rate_etfs(tickers[i])

    '''
    return True

if __name__ == "__main__":
    initialize(sys.argv)
