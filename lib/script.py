from . import stocks_to_buy
from . import get_trading_dataframes

import zipfile
from urllib.request import urlopen
import pandas as pd
from datetime import date
from io import BytesIO
from deta import Deta
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

deta_id = os.getenv("DETA")

# Initialize with a Project Key
deta = Deta(deta_id)

def script():

    people = deta.Base("People") #Retrieve people of interest
    people_df = pd.DataFrame.from_dict(people.fetch().items) 

    todays_date = date.today()

    todays_date_formatted = todays_date.strftime("%d/%m/%y")
    
    # fetching the current year
    year = todays_date.year
    zip_file_url=f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.ZIP" 
    pdf_file_url=f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/"
    
    r = urlopen(zip_file_url)

    zipdata = BytesIO(r.read())
    myzipfile = zipfile.ZipFile(zipdata)
    fd = myzipfile.open(f'{year}FD.txt')
    readable = BytesIO(fd.read())
    fd.close()
    
    financial_disclosure_df = pd.read_csv(readable, sep='\t')
    financial_disclosure_df['FilingDate'] = pd.to_datetime(financial_disclosure_df['FilingDate'])

    #retrieve dataframes that contain new trades by people of interest
    trading_dataframes = get_trading_dataframes.gettradingdataframes(financial_disclosure_df, people_df, pdf_file_url)

    people = deta.Base("People") #reinitialise
    stocks = []
    for key in trading_dataframes:
        try:
            person = people.get(key)
            first_name = person["first_name"]
            last_name = person["last_name"]
            new_doc_id = person["last_doc_id"]
            name = f"{first_name} {last_name}"
            tickers_to_buy, tickers_to_sell = stocks_to_buy.alpaca_translation(trading_dataframes[key], name, new_doc_id, str(todays_date_formatted))
            ticker_string = ", ".join(tickers_to_buy)
            if len(tickers_to_buy) != 0:
                print(f"{name} purchased: {ticker_string}\n")
                for ticker in tickers_to_buy:
                    stocks.append(ticker)
        except Exception as err:
            print(err)
            print(key)

    stocks = list(set(stocks))

    return stocks