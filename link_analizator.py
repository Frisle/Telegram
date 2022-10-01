import requests


def ticker():
    req = requests.get("https://cdn.cur.su/api/nbkz.json")
    responce = req.json()
    sell_price_usd = responce["rates"]["USD"]
    sell_price_kzt = responce["rates"]["KZT"]
    sell_price_euro = responce["rates"]["EUR"]
    result_usd = sell_price_kzt / sell_price_usd
    result_euro = sell_price_kzt / sell_price_euro
    return round(result_usd, 2), round(result_euro, 2)





