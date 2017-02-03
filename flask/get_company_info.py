from yahoo_finance import Share
import csv
import sqlite3
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "fortune500.db")


def get_stock_symbols(file_name):
    symbols = []
    with open(file_name, 'r') as file:
        file_reader = csv.reader(file, delimiter=',', quotechar='|')
        for row in file_reader:
            if len(row[0]) < 6:
                symbols.append((row[0], row[1]))
    return symbols


def get_stock_info(stock_symbol):
    _stock_info = dict()
    stock = Share(stock_symbol)
    _stock_info['price'] = stock.get_price()
    _stock_info['market_cap'] = stock.get_market_cap()
    _stock_info['price_earnings'] = stock.get_price_earnings_ratio()
    return _stock_info


def get_all_stocks():
    symbols = get_stock_symbols('Fortune500Companies.csv')
    stock_info = dict()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for symbol, name in symbols:
        stock_info[symbol] = get_stock_info(symbol)
        stock_info[symbol]['name'] = name
        cursor.execute("""INSERT OR REPLACE INTO basic VALUES(?, ?, ?, ?, ?)""", (symbol, stock_info[symbol]['name'], stock_info[symbol]["price"], stock_info[symbol]["market_cap"], stock_info[symbol]["price_earnings"]))
    conn.commit()
    conn.close()

get_all_stocks()

