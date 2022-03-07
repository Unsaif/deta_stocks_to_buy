from fastapi import FastAPI
from lib import script
from deta import Deta
from pydantic import BaseModel

# Initialize with a Project Key
deta = Deta("a0zd0kwp_zP8cFJdLzpuSB3YR7N9TyAjbR2LYaeQp")
people = deta.Base("People")
trades = deta.Base("Trades")

app = FastAPI()

@app.get("/stocks_to_buy")
async def stocks_to_buy():
    stonks = script.script()
    return stonks

@app.get("/trades") #TODO get specific trades
async def read_trades():
    all_trades = trades.fetch().items
    return all_trades

class Person(BaseModel):
    last_name: str
    first_name: str
    last_doc_id: str

@app.post('/add_person')
async def add_person(person: Person):
    people.put(person.dict())
    return person

#TODO update person

