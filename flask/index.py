from flask import Flask
import sqlite3
from flask_table import Table, Col
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "fortune500.db")


# Declare your table
class ItemTable(Table):
    symbol = Col('Symbol')
    name = Col('Name')
    price = Col('Price')
    mkt_cap = Col('Market Cap')
    pe = Col('Price Earnings')

# Get some objects
class Item(object):
    def __init__(self, symbol, name, price, mkt_cap, pe):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.mkt_cap = mkt_cap
        self.pe = pe
app = Flask(__name__)


@app.route('/')
def test():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('SELECT * FROM basic')
    x = cur.fetchall()
    y = [Item(a, b, c, d, e) for a,b,c,d,e in x]
    table = ItemTable(y)
    return table.__html__()

if __name__ == '__main__':
    app.run()