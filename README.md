MEXC Triangular Arbitrage Bot

This repository contains a Python script designed to perform triangular arbitrage on the MEXC Exchange. The bot fetches prices for specified trading pairs, calculates potential arbitrage opportunities, and executes trades if profitable.

Features:
Fetches account information from MEXC.
Retrieves current prices for specified trading pairs.
Places limit orders on MEXC.
Executes triangular arbitrage strategy.

Prerequisites:
Python 3.x
MEXC Exchange account with API access


Installation

Clone the repository:
bash
git clone https://github.com/yourusername/mexc-triangular-arbitrage-bot](https://github.com/coqui123/mexc-triangular-arbitrage-.git
cd mexc-triangular-arbitrage-bot

Install the required Python packages:
bash
pip install requests
pip install mexc-sdk

Setup
Configure your environment variables:
Create a .env file in the root directory of the project and add your MEXC API key and secret:
In plaintext
MEXC_API_KEY = 'your_mexc_api_key'
MEXC_SECRET_KEY = 'your_mexc_api_secret'

Update the constants in the script:
Open the main.py file and set the placeholder values for MAKER_FEE and TAKER_FEE to the current fees.
Usage
Run the script:
bash
python main.py

The script will continuously check for arbitrage opportunities and execute trades if profitable.

Functions:
create_mexc_signature(params, secret_key)
Creates a signature for MEXC API requests.

get_mexc_account_info()
Fetches account information from MEXC.

get_mexc_price(symbol)
Retrieves the current price for a specified trading pair.

place_limit_order(symbol, side, quantity, price)
Places a limit order on MEXC.

execute_triangular_arbitrage()
Executes the triangular arbitrage strategy by fetching prices, calculating potential profit, and placing trades if profitable.

Logging
The script uses Python's built-in logging module to log information and errors. Logs are printed to the console with timestamps.

Disclaimer
This application is provided for educational purposes only. Use it at your own risk. The authors are not responsible for any financial losses incurred as a result of using this application. Enjoy trading on MEXC!
