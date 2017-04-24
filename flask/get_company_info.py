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
    if _stock_info['market_cap'] is not None:
        _stock_info['market_cap'] = _stock_info['market_cap'].replace("B", "")
    _stock_info['price_earnings'] = stock.get_price_earnings_ratio()
    return _stock_info


def get_stock_historical(stock_symbol, date_one, date_two):
    stock_info = dict()
    stock = Share(stock_symbol)
    stock_hist = stock.get_historical(date_one, date_two)
    return stock_hist


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


def save_stocks_to_file(open_file_name, save_file_name, start_date, end_date):
    symbols = get_stock_symbols(open_file_name)
    stock_info = dict()
    with open(save_file_name, 'w') as save_file:
        writer = csv.writer(save_file, delimiter=',', quotechar='|')
        writer.writerow(["date", "name", "symbol", "high", "low", "close", "adj close", "volume", "high market cap",
                         "low market cap", "close market cap", "adj close market cap"])
        for symbol, name in symbols:
            try:
                stock_info = get_stock_historical(symbol, start_date, end_date)
                for stock in stock_info:
                    writer.writerow([stock['Date'],
                                     name,
                                     stock['Symbol'],
                                     stock['High'],
                                     stock['Low'],
                                     stock['Close'],
                                     stock['Adj_Close'],
                                     stock['Volume'],
                                     float(stock['High']) * float(stock['Volume']),
                                     float(stock['Low']) * float(stock['Volume']),
                                     float(stock['Close']) * float(stock['Volume']),
                                     float(stock['Adj_Close']) * float(stock['Volume'])])
            except Exception:
                print("There was a problem but we ignored it")


# get_all_stocks()
save_stocks_to_file("Fortune500Companies.csv", "Stocks.csv", '2008-01-01', '2017-3-15')
