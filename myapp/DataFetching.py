import requests
import sqlite3

#Add unitest

def connect():
    database = sqlite3.connect('db.sqlite3', isolation_level=None, timeout=10)
    return database


stocksDatabase = connect()

def fetch_stock(symbol):
    url = "https://sandbox.iexapis.com/stable/stock/" + str(
symbol) + "/quote?token=Tpk_087a52e2547e449e9cee8748f00491eb"
    response = requests.get(url)
    if (response.status_code) == 404:
        return None
    else:
        dataset = response.json()
    return (dataset)


def is_cached(ssymbol):
    c1 = stocksDatabase.cursor()
    res = list(c1.execute('''select symbol from stocks '''))
    print(res)
    res = flatter(res)

    if ssymbol in res:
        return True
    else:
        return False


def add_stock_to_db(symbol):
    if is_cached(symbol.upper()) is True:
        return None
    else:
        stock_data = fetch_stock(symbol)
        if stock_data == 0:
            exit(0)
        else:
            c1 = stocksDatabase.cursor()
            c1.execute("INSERT INTO stocks VALUES (?,?)", [stock_data["symbol"], stock_data["companyName"]])


def flatter(tu):
    l = []
    for i in tu:
        l.append(i[0])
    return l
