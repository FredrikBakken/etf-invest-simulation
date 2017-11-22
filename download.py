#!/usr/bin/env python3
# -*- coding: utf-8 -*

import os
import time
import contextlib

from bs4 import BeautifulSoup
from urllib.request import urlopen


def check_codec(v):
    variable = v

    if b"\xf8" in variable:
        variable = variable.replace(b'\xf8', b'o')
    elif b"\xd8" in variable:
        variable = variable.replace(b'\xd8', b'O')
    elif b"\xe5" in variable:
        variable = variable.replace(b'\xe5', b'a')
    elif b"\xe6" in variable:
        variable = variable.replace(b'\xe6', b'ae')

    return variable


def download_etfs():
    # Counter variables
    pages = 0
    number_of_etfs = 0

    # List variables
    ticker = []
    company = []
    currency = []
    asset_manager = []
    investment_area = []
    no_data_list = []

    # URL string variables
    list_url = "http://www.netfonds.no/quotes/funds.php?sort=NAME&exchange=FOND&reversep=T&area=&type=" \
               "&currency=&manager=&tradeablep=N&name=&page_size=500&page="
    fund_url = "http://www.netfonds.no/quotes/fund.php?paper="
    hist_url = "http://www.netfonds.no/quotes/paperhistory.php?paper="

    # File and directory specific variables
    etfs_dir = 'data/etf-list/'
    etfs_fil = 'active_etfs.json'
    etfs_file = etfs_dir + etfs_fil
    hist_dir = 'data/historical-values/'

    # Create directory if it does not exist
    if not os.path.exists(etfs_dir):
        os.makedirs(etfs_dir)

    if not os.path.exists(hist_dir):
        os.makedirs(hist_dir)

    # Delete old ETF list
    with contextlib.suppress(FileNotFoundError):
        os.remove(etfs_file)

    # Start Beautifulsoup
    list_content = urlopen(list_url + str(pages + 1)).read()
    list_soup = BeautifulSoup(list_content, "html.parser")

    # Find the number of pages
    for option in list_soup.find_all('option'):
        if "Side" in option.text:
            pages = pages + 1

    # Loop through all pages to get company and ticker
    for page in range(pages):
        list_content = urlopen(list_url + str(page + 1)).read()
        list_soup = BeautifulSoup(list_content, "html.parser")

        # Find all links with ticker and company info
        for a in list_soup.find_all('a', href=True):
            s = a['href']
            start = "ppaper.php?paper="
            end = "&exchange=FOND"
            if start in a['href']:
                number_of_etfs = number_of_etfs + 1
                c = a.text.encode('ISO-8859-1', 'ignore')
                c = check_codec(c).decode('ISO-8859-1')
                t = s[s.find(start) + len(start):s.rfind(end)]
                ticker.append(t)
                company.append(c)

    # Loop through the tickers and get missing information for all etfs
    for t in range(len(ticker)):
        # Avoid DDoS
        time.sleep(1)

        # Get current ticker
        current_ticker = ticker[t]

        # Filename for downloading historical values
        hist_fil = current_ticker + ".csv"
        hist_file = hist_dir + hist_fil

        print(str(t) + " | Downloading to " + hist_file)

        # Access website for downloading values
        response = urlopen(hist_url + current_ticker + ".FOND&csv_format=csv")
        html = response.read()

        # Checking if historical value data is empty or not
        if b'quote_date,paper,exch,open,high,low,close,volume,value\n' == html:
            no_data_list.append(current_ticker)
        else:
            # Writing values to file
            with open(hist_file, 'wb') as f:
                f.write(html)

        # Local boolean variables
        found_currency = False
        found_asset_manager = False
        found_investment_area = False

        # Setting up content crawler
        fund_content = urlopen(fund_url + str(ticker[t]) + '.FOND')
        fund_soup = BeautifulSoup(fund_content, "html.parser")

        # Loop through all table elements
        for row in fund_soup.find_all('tr'):
            # Local string variables
            title = ''
            content = ''

            # Find table element title
            if row.th is not None:
                t = row.th.text.encode('ISO-8859-1', 'ignore')
                title = check_codec(t).decode('ISO-8859-1')

            # Find table element content
            if row.td is not None:
                c = row.td.text.encode('ISO-8859-1', 'ignore')
                content = check_codec(c).decode('ISO-8859-1')

            # Appending currency, asset manager, and investment area to lists
            if title == "Valuta":
                currency.append(content)
                found_currency = True
            elif title == "Forvalter":
                asset_manager.append(content)
                found_asset_manager = True
            elif title == "Investeringsomrade":
                investment_area.append(content)
                found_investment_area = True

            # If all elements found, download historical values and go to next ticker
            if (found_currency) and (found_asset_manager) and (found_investment_area):
                # Go to next ticker
                continue

    # Write all information to csv file for storing
    with open(etfs_file, "w") as f:
        for i in range(len(ticker)):
            insert = True

            for j in range(len(no_data_list)):
                if no_data_list[j] in ticker[i]:
                    insert = False

            if insert:
                f.write(ticker[i] + ',' + company[i] + ',' + currency[i] + ',' + asset_manager[i] + ',' +
                        investment_area[i] + '\n')

    return True
