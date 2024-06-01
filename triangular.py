import requests
import time
import hashlib
import hmac
import logging
from mexc_sdk import Spot

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for MEXC
MEXC_API_KEY = 
MEXC_SECRET_KEY =
MEXC_BASE_URL = 'https://api.mexc.com'

# Placeholder values for maker and taker fees (in percentage)
MAKER_FEE = 0.0  # Example: 0.1% maker fee
TAKER_FEE = 0.1  # Example: 0.1% taker fee

# Initialize MEXC Spot client
client = Spot(api_key=MEXC_API_KEY, api_secret=MEXC_SECRET_KEY)

# Function to create a signature for MEXC
def create_mexc_signature(params, secret_key):
    query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# Function to get account info from MEXC
def get_mexc_account_info():
    endpoint = '/api/v3/account'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
    }
    params['signature'] = create_mexc_signature(params, MEXC_SECRET_KEY)
    headers = {
        'X-MEXC-APIKEY': MEXC_API_KEY
    }
    url = MEXC_BASE_URL + endpoint
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching account info from MEXC: {response.status_code} - {response.text}")
        return None

# Function to get price from MEXC
def get_mexc_price(symbol):
    url = f"{MEXC_BASE_URL}/api/v3/ticker/price"
    params = {'symbol': symbol}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return float(response.json()['price'])
    else:
        logging.error(f"Error fetching price from MEXC: {response.status_code} - {response.text}")
        return None

# Function to place a limit order on MEXC
def place_limit_order(symbol, side, quantity, price):
    try:
        order = client.new_order(symbol=symbol, side=side, order_type='LIMIT', options={'quantity': quantity, 'price': price, 'timeInForce': 'GTC'})
        logging.info(f"Limit order placed: {order}")
        return order
    except Exception as e:
        logging.error(f"Error placing limit order: {e}")
        return None

# Function to execute triangular arbitrage on MEXC
def execute_triangular_arbitrage():
    # Fetch prices for the pairs
    btc_usdt_price = get_mexc_price('BTCUSDT')
    eth_usdt_price = get_mexc_price('ETHUSDT')
    eth_btc_price = get_mexc_price('ETHBTC')

    if btc_usdt_price and eth_usdt_price and eth_btc_price:
        # Calculate potential arbitrage profit
        initial_usd = 1500  # Example initial amount in USD
        btc_amount = initial_usd / btc_usdt_price
        eth_amount = btc_amount / eth_btc_price
        final_usd = eth_amount * eth_usdt_price

        # Account for maker and taker fees
        maker_fee_amount = initial_usd * (MAKER_FEE / 100)
        taker_fee_amount = final_usd * (TAKER_FEE / 100)
        net_profit = final_usd - initial_usd - maker_fee_amount - taker_fee_amount

        logging.info(f"Initial USD: {initial_usd}, Final USD: {final_usd}, Net Profit: {net_profit}")

        if net_profit > 0:
            logging.info("Arbitrage opportunity found! Executing trades...")
            # Execute trades with limit orders
            place_limit_order('BTCUSDT', 'BUY', initial_usd / btc_usdt_price, btc_usdt_price)
            place_limit_order('ETHBTC', 'BUY', btc_amount / eth_btc_price, eth_btc_price)
            place_limit_order('ETHUSDT', 'SELL', eth_amount, eth_usdt_price)
        else:
            logging.info("No arbitrage opportunity found.")

# Main function
def main():
    # Check balances on MEXC
    mexc_account_info = get_mexc_account_info()
    if mexc_account_info:
        logging.info("MEXC Account Info:")
        for balance in mexc_account_info['balances']:
            logging.info(f"Asset: {balance['asset']}, Free: {balance['free']}, Locked: {balance['locked']}")

    while True:
        # Execute triangular arbitrage
        execute_triangular_arbitrage()
        time.sleep(10)

if __name__ == "__main__":
    main()
