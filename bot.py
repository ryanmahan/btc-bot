import robin_stocks as r
import time, functools
from auth import username, password
login = r.login(username, password)

def get_btc_price():
  return r.get_crypto_quote("BTC")["mark_price"];

def get_btc_held():
  btc_holding = list(filter(lambda x: x["currency"]["code"] == "BTC", r.get_crypto_positions()))[0];
  btc_held = btc_holding["quantity_available"]
  return btc_held

def get_usd_held():
  return r.load_account_profile("buying_power")

def print_status(prev_price, curr_price, btc_held, usd_held):
  print("prev, curr: ", prev_price, curr_price)
  print("BTC Holdings, USD Holdings", btc_held, usd_held)

curr_price = get_btc_price();
btc_holding = list(filter(lambda x: x["currency"]["code"] == "BTC", r.get_crypto_positions()))[0];
btc_held = btc_holding["quantity_available"]
usd_held = get_usd_held()
print_status("?", curr_price, btc_held, usd_held);
time.sleep(30);

while(True):
  prev_price = curr_price
  curr_price = get_btc_price()
  print("prev, curr: ", prev_price, curr_price)
  print("BTC Holdings, USD Holdings", btc_held, usd_held)
  btc_held = get_btc_held()
  usd_held = get_usd_held()
  percent_change = (curr_price - prev_price)/curr_price
  # has increased, dont have bitcoin
  if (percent_change > 0.00075 and float(usd_held) > 0):
    # buy bitcoin, or hold
    print(r.order_crypto("BTC", "buy", float(usd_held), "price"))
    btc_held = get_btc_held()
    print("Bought ", str(btc_held), " BTC at: ", str(curr_price))
  elif (float(btc_held) > 0):
    # sell bitcoin, or wait
    btc_held = get_btc_held()
    print("Bought " + str(btc_held) + " BTC at: ", str(curr_price))
    print(r.order_crypto("BTC", "sell", btc_held));
    
  time.sleep(5*60);