import pandas as pd
from deta import Deta
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

deta_id = os.getenv("DETA")

# Initialize with a Project Key
deta = Deta(deta_id)

def alpaca_translation(df, name, doc_id, date): #finds tickers to buy for alpaca
    trades = deta.Base("Trades")
    
    tickers_to_purchase = []
    tickers_to_sell = []

    for i, entry in df.iterrows():
        ticker = entry["Ticker"]
        if not pd.isnull(ticker):
            body = {"name": name, "type": entry["Type"], "ticker": ticker, "date": date, "doc_id": doc_id} 
            trades.put(body) #adding trade to database

            if entry["Type"] == "P" and "call options" not in entry["Description"]:
                tickers_to_purchase.append(ticker)
            else:
                tickers_to_sell.append(ticker)

    return set(tickers_to_purchase), set(tickers_to_sell)