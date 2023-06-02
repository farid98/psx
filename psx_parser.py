# This script willparse the latest stock price, dividend yield, and a few other fields for selected stocks
# The stock symbols to be parsed should be in a CSV file caleed stocks.csv in the same folder
# The output will be placed in another CSV file called psx_output.csv - this csv can be opened directly in Excel

# BEFORE you run it, make sure you have a stocks.csv file with the stocks symbols you want to parse in the same directory - and example file is provided
# after you run it, look for a psx_output.csv file in the directory - then open it straight into Excel
# once you have it in Excel you can of course do anything with it


# You will need to INSTALL two libraries for this to work
#       beautifulsoup -  install with pip using this command: pip install beautifulsoup4
#       requests - install with pip command: pip install requests


import requests
from bs4 import BeautifulSoup 
import csv
from datetime import date
from datetime import datetime


# Initialize an empty array to store the concatenated values
concatenated_values = []

# This page on psx contains all the latest data we want to fetch
page = "https://dps.psx.com.pk/screener"


# The names of the stocks we want to parse should be stored in a csv file called stocks.csv in the same directory
# Read the values from the CSV file and place them in an array
with open('psx_stocks.csv', 'r') as file:
    reader = csv.reader(file)
    
    for row in reader:
        print(row)
        value = row[0]
        concatenated_value = value
        concatenated_values.append(concatenated_value)

stocks = concatenated_values

#get the psx page which we will parse - we use beautifulSoup for this
response = requests.get(page)
soup = BeautifulSoup(response.content, 'html.parser')


# Initialize an empty array to store the values we parse
stock_details = []

# Loop through each page and extract the value of the 'quote__close' class
for stock in stocks:

    stock_row = soup.find('td', {'data-order': stock})

    stock_row_relevantcolumns = stock_row.find_next_siblings('td', limit=8)

    #we have the right row and all the columns <td> elemenst which contain the various data points we need - just grab them one by one

    price = stock_row_relevantcolumns[3]
    price_value = price.text.strip()

    year_change = stock_row_relevantcolumns[5]
    year_change_value = year_change.text.strip()

    pe_ratio = stock_row_relevantcolumns[6]
    pe_ratio_value =pe_ratio.text.strip()

    dividend_yield = stock_row_relevantcolumns[7]
    dividend_yield_value = dividend_yield.text.strip()

    stockLine = (stock , price_value, year_change_value, dividend_yield_value, pe_ratio_value)
    stock_details.append(stockLine)


# we also store current date so that CSV will have a record of when the data was refreshed
today = datetime.now()
date_string = today.strftime("%d/%m/%Y  %H:%M") 



# We have everything we need - now just write it to the output file
with open('psx_output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    n = writer.writerow([date_string])
    writer.writerow(['Stock','Price', 'Year change','Dividend Yield', 'PE Ratio' ])
    writer.writerows(stock_details)

